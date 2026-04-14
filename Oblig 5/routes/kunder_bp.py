from flask import render_template, redirect, url_for, request, Blueprint, jsonify
from flask_login import login_required, current_user
from database import Database
from models import Kunde
from mysql.connector import IntegrityError

kunder_bp = Blueprint('kunder',__name__)

@kunder_bp.route('/')
@login_required
def all():
    with Database() as db:
        kunder_raw = db.get_all_kunder()

        kunder = []

        for kunde in kunder_raw:
            kundenr = kunde[0]

            # -------- telefon --------
            telefoner_raw = db.get_telefoner_for_kunde(kundenr)
            telefoner = [t[0] for t in telefoner_raw]


            # -------- navn --------
            navn = ""

            privat = db.get_privatkunde_navn(kundenr)
            if privat:
                navn = privat[0] + " " + privat[1]
            else:
                bedrift = db.get_bedriftkunde_navn(kundenr)
                if bedrift:
                    navn = bedrift[0]

            # -------- adresse --------
            fakt_adr_raw = db.get_adresse_by_id(kunde[2])
            lev_adr_raw = db.get_adresse_by_id(kunde[3])

            print("FAKT_ADRESSE:", fakt_adr_raw)

            fakt_adresse = ""
            levering_adresse = ""

            if fakt_adr_raw:
                fakt_adresse = f"{fakt_adr_raw[0]} {fakt_adr_raw[1]}, {fakt_adr_raw[2]} {fakt_adr_raw[3]}"

            if lev_adr_raw:
                levering_adresse = f"{lev_adr_raw[0]} {lev_adr_raw[1]}, {lev_adr_raw[2]} {lev_adr_raw[3]}"
            # -------- objekt --------
            kunde_obj = Kunde(
                kunde[0],
                kunde[1],
                kunde[2],
                kunde[3],
                telefoner,
                navn,
                fakt_adresse,
                levering_adresse
            )

            kunder.append(kunde_obj)

    return render_template('Kunder/read.html', kunder=kunder)


@kunder_bp.route('/check_kundenr')
@login_required
def check_kundenr():
    kundenr = request.args.get('kundenr')

    with Database() as db:
        kunde = db.get_kunde_by_kundenr(kundenr)

    return jsonify({'exists': kunde is not None})


@kunder_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_kunde():
    error = None

    if request.method == 'POST':
        kundenr = request.form['kundenr']
        kundetype = request.form['kundetype']
        fornavn = request.form.get('fornavn', '')
        etternavn = request.form.get('etternavn', '')
        kundenavn = request.form.get('kundenavn', '')
        epost = request.form['epost']
        mobil = request.form['mobil']
        fakt_adresse = request.form['fakt_adresse']
        levering_adresse = request.form['levering_adresse']

        print("FAKT_ADRESSE_FORM:", repr(fakt_adresse))
        print("LEVERING_ADRESSE_FORM:", repr(levering_adresse))

        fakt_split = [x.strip() for x in fakt_adresse.split(',')]
        lev_split = [x.strip() for x in levering_adresse.split(',')]

        print("FAKT_SPLIT:", fakt_split)
        print("LEV_SPLIT:", lev_split)


        if len(fakt_split) != 3 or len(lev_split) != 3:
            error = 'Adresse må være på format: Gate, Nummer, PostNr'

            kunde_obj = Kunde(
                kundenr,
                epost,
                0,
                0,
                [mobil] if mobil else [],
                "",
                fakt_adresse,
                levering_adresse
            )

            kunde_obj.kundetype = kundetype
            kunde_obj.fornavn = fornavn
            kunde_obj.etternavn = etternavn
            kunde_obj.kundenavn = kundenavn

            return render_template('Kunder/add_edit.html', kunde=kunde_obj, error=error)


        fakt_gate = fakt_split[0]
        fakt_nr = fakt_split[1]
        fakt_postnr = fakt_split[2]

        lev_gate = lev_split[0]
        lev_nr = lev_split[1]
        lev_postnr = lev_split[2]

        try:
            with Database() as db:
                max_adresse_id = db.get_max_adresse_id()[0]
                if max_adresse_id is None:
                    max_adresse_id = 0

                fakt_adresse_id = max_adresse_id + 1
                levering_adresse_id = max_adresse_id + 2

                db.add_adresse(fakt_adresse_id, 1, fakt_postnr, fakt_gate, fakt_nr)
                db.add_adresse(levering_adresse_id, 2, lev_postnr, lev_gate, lev_nr)

                db.add_kunde(kundenr, epost, fakt_adresse_id, levering_adresse_id)
                db.add_kundetelefon(kundenr, mobil)

                if kundetype == 'privat':
                    db.add_privatkunde(kundenr, fornavn, etternavn)
                elif kundetype == 'bedrift':
                    db.add_bedriftkunde(kundenr, kundenavn)

            return redirect(url_for('kunder.all'))

        except IntegrityError:

            error = 'KundeNr finnes allerede. Velg et annet kundenummer.'

            kunde_obj = Kunde(

                kundenr,

                epost,

                0,

                0,

                [mobil] if mobil else [],

                "",

                fakt_adresse,

                levering_adresse

            )

            kunde_obj.kundetype = kundetype

            kunde_obj.fornavn = fornavn

            kunde_obj.etternavn = etternavn

            kunde_obj.kundenavn = kundenavn

            return render_template('Kunder/add_edit.html', kunde=kunde_obj, error=error)

    return render_template('Kunder/add_edit.html', kunde=None, error=error)


@kunder_bp.route('/edit/<int:kundenr>', methods=['GET', 'POST'])
@login_required
def edit_kunde(kundenr):
    error = None

    if request.method == 'POST':
        kundenr = request.form['kundenr']
        kundetype = request.form['kundetype']
        fornavn = request.form.get('fornavn', '')
        etternavn = request.form.get('etternavn', '')
        kundenavn = request.form.get('kundenavn', '')
        epost = request.form['epost']
        mobil = request.form['mobil']
        fakt_adresse = request.form['fakt_adresse']
        levering_adresse = request.form['levering_adresse']

        fakt_split = [x.strip() for x in fakt_adresse.split(',')]
        lev_split = [x.strip() for x in levering_adresse.split(',')]

        if len(fakt_split) != 3 or len(lev_split) != 3:
            error = 'Adresse må være på format: Gate, Nummer, PostNr'
        else:
            fakt_gate = fakt_split[0]
            fakt_nr = fakt_split[1]
            fakt_postnr = fakt_split[2]

            lev_gate = lev_split[0]
            lev_nr = lev_split[1]
            lev_postnr = lev_split[2]

            with Database() as db:
                kunde_raw = db.get_kunde_by_kundenr(kundenr)

                if not kunde_raw:
                    return "Kunde ikke funnet"

                fakt_adresse_id = kunde_raw[2]
                levering_adresse_id = kunde_raw[3]

                db.update_adresse(fakt_adresse_id, fakt_postnr, fakt_gate, fakt_nr)
                db.update_adresse(levering_adresse_id, lev_postnr, lev_gate, lev_nr)

                db.update_kunde(kundenr, epost, fakt_adresse_id, levering_adresse_id)
                db.update_kundetelefon(kundenr, mobil)

                if kundetype == 'privat':
                    db.update_privatkunde(kundenr, fornavn, etternavn)
                elif kundetype == 'bedrift':
                    db.update_bedriftkunde(kundenr, kundenavn)

            return redirect(url_for('kunder.all'))

    with Database() as db:
        kunde_raw = db.get_kunde_by_kundenr(kundenr)

        if not kunde_raw:
            return "Kunde ikke funnet"

        telefoner_raw = db.get_telefoner_for_kunde(kundenr)
        telefoner = [t[0] for t in telefoner_raw]

        navn = ""
        fornavn = ""
        etternavn = ""
        kundenavn = ""
        kundetype = ""

        privat = db.get_privatkunde_navn(kundenr)
        if privat:
            fornavn = privat[0]
            etternavn = privat[1]
            navn = privat[0] + " " + privat[1]
            kundetype = "privat"
        else:
            bedrift = db.get_bedriftkunde_navn(kundenr)
            if bedrift:
                kundenavn = bedrift[0]
                navn = bedrift[0]
                kundetype = "bedrift"

        fakt_adr_raw = db.get_adresse_by_id(kunde_raw[2])
        lev_adr_raw = db.get_adresse_by_id(kunde_raw[3])

        fakt_adresse = ""
        levering_adresse = ""

        if fakt_adr_raw:
            fakt_adresse = f"{fakt_adr_raw[0]}, {fakt_adr_raw[1]}, {fakt_adr_raw[2]}"

        if lev_adr_raw:
            levering_adresse = f"{lev_adr_raw[0]}, {lev_adr_raw[1]}, {lev_adr_raw[2]}"

        kunde_obj = Kunde(
            kunde_raw[0],
            kunde_raw[1],
            kunde_raw[2],
            kunde_raw[3],
            telefoner,
            navn,
            fakt_adresse,
            levering_adresse
        )

        kunde_obj.kundetype = kundetype
        kunde_obj.fornavn = fornavn
        kunde_obj.etternavn = etternavn
        kunde_obj.kundenavn = kundenavn

    return render_template('Kunder/add_edit.html', kunde=kunde_obj, error=error)


