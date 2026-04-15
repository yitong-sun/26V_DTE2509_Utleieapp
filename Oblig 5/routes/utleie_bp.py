from flask import render_template, redirect, url_for, request, Blueprint, flash
from flask_login import login_required, current_user
from database import Database
from models import Utleie, AddUtleieForm, UpdateUtleieForm
#from datetime import datetime, date

utleie_bp = Blueprint('utleie',__name__)

@utleie_bp.route('/utleie', methods=['GET', 'POST'])
@login_required
def all():
    with Database() as db:
        utleier = [Utleie(*utleie) for utleie in db.get_all_utleie()] #not implemented in Database yet

    return render_template('utleie/read.html', utleier=utleier)

@utleie_bp.route('/utleie/add', methods=['GET', 'POST'])
@login_required
def add_utleie():
    with Database() as db:
        kunde_nrs = db.get_kunde_nr()
        avail_utstyr = db.get_utstyr_if_available()
        betalingsmåter = db.get_betalingsmåter()

        if not avail_utstyr:
            error = "Ingen utstyr tilgjengelig"
            utleier = [Utleie(*utleie) for utleie in db.get_all_utleie()]
            return render_template('utleie/read.html', utleier=utleier, error=error)

    form = AddUtleieForm()
    form.kunde_nr.choices = [(k[0], k[0]) for k in kunde_nrs]
    form.avail_utstyr.choices = [(u[0], u[0]) for u in avail_utstyr]
    form.betalings_måte.choices = [(b[0], b[0]) for b in betalingsmåter]

    if request.method == "POST":
        leveres_kunde = request.form['leveres_kunde']
        leveringskostnad = request.form.get('leveringskostnad', 0)
        lev_kost = leveringskostnad if leveringskostnad != '' else 0
        if int(lev_kost)<0:
            return render_template('utleie/create.html', form=form, utleie=None, error="Leveringskostnad kan ikke være negativ")

    if form.validate_on_submit():
        with Database() as db:
                
                betalingsmåte_id = db.get_betalingsmåte_id(form.betalings_måte.data)[0]
                utstyr_id,instans_id = form.avail_utstyr.data.split(".")
                db.add_utleie(current_user.id, form.kunde_nr.data, utstyr_id, instans_id, leveres_kunde ,betalingsmåte_id, form.start_dato.data, lev_kost)
                return redirect(url_for('utleie.all'))
    return render_template('utleie/create.html', form=form, utleie=None)

@utleie_bp.route('/utleie/edit/<int:utleie_id>', methods=['GET', 'POST'])
@login_required
def edit_innlevert_utleie(utleie_id):
    form = UpdateUtleieForm()
    if form.validate_on_submit():
         slutt_dato = form.slutt_dato.data
         with Database() as db:
                utleid_dato = db.get_utleid_dato(utleie_id)[0]
                duration = slutt_dato - utleid_dato
                if duration.days < 0:
                     return render_template('utleie/add_edit.html', form=form, 
                                            error="Kan ikke velge innleveringsdato som er tidligere en utleiddato")
                else:
                    db.edit_innlevert_utleie(slutt_dato,utleie_id)
                    totalpris= db.calculate_totalpris(utleie_id)[0]
                    db.edit_totalpris_utleie(totalpris, utleie_id)
                    return redirect(url_for('utleie.all'))
    return render_template('utleie/add_edit.html', form=form)


""" Registrere utleie
        *Velg kunde
        *Velg Utstyr(kun tilgjengelig)
        *Sett dato
        *Automatisk registrer hvilken ansatt som ekspederer

    Registrer innlevering
        *Marker utleie som levert
        *Sett innleveringsdato  """