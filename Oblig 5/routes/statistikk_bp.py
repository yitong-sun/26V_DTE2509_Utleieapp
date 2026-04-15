from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utstyr_Inntekt, Utleie_Aktiv, Utstyr_Antall_Utleid

statistikk_bp = Blueprint('statistikk',__name__, url_prefix='/statistikk')



@statistikk_bp.route('/')
@login_required
def all_statistikk():
    with Database() as db:

        #A kundeliste
        kunder_raw = db.get_all_kunder()
        kunder = []

        for kunde in kunder_raw:
            kundenr = kunde[0]

            telefoner_raw = db.get_telefoner_for_kunde(kundenr)
            telefoner = [t[0] for t in telefoner_raw]

            navn = ""

            privat = db.get_privatkunde_navn(kundenr)
            if privat:
                navn = privat[0] + " " + privat[1]
            else:
                bedrift = db.get_bedriftkunde_navn(kundenr)
                if bedrift:
                    navn = bedrift[0]

            fakt_adr_raw = db.get_adresse_by_id(kunde[2])
            lev_adr_raw = db.get_adresse_by_id(kunde[3])

            fakt_adresse = ""
            levering_adresse = ""

            if fakt_adr_raw:
                fakt_adresse = f"{fakt_adr_raw[0]} {fakt_adr_raw[1]}, {fakt_adr_raw[2]} {fakt_adr_raw[3]}"

            if lev_adr_raw:
                levering_adresse = f"{lev_adr_raw[0]} {lev_adr_raw[1]}, {lev_adr_raw[2]} {lev_adr_raw[3]}"

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

        #B aktive utleier
        aktive_utleier = [Utleie_Aktiv(*utleie) for utleie in db.aktive_utleier(current_user.id)]
        kundebehandler_navn = db.get_kundebehandler_navn(current_user.id)[0]
        #C Komplette utleier
        antall_komplette_utleier = db.komplette_utleier()[0]
        #D Innetkt per utstyr
        utstyrer = [Utstyr_Inntekt(*utstyr) for utstyr in db.tjent_per_utstyr()]
        #E Flest utleid Utstyr
        flest_utleid_utstyrer = [Utstyr_Antall_Utleid(*utstyr) for utstyr in db.flest_utleid_utstyr()]
        flest_antall = db.get_top_flest_utleid_utstyr_antall()[0]

    return render_template('Statistikk/read.html',
                           #variabler:
                           kunder=kunder,
                           utstyrer=utstyrer, 
                           antall_komplette_utleier=antall_komplette_utleier,
                           aktive_utleier= aktive_utleier,
                           kundebehandler_navn= kundebehandler_navn,
                           flest_utleid_utstyrer=flest_utleid_utstyrer,
                           flest_antall=flest_antall)


