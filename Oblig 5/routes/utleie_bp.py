from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utleie, AddUtleieForm, UpdateUtleieForm
import datetime

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

    form = AddUtleieForm()
    form.kunde_nr.choices = [(k[0], k[0]) for k in kunde_nrs]
    form.avail_utstyr.choices = [(u[0], u[0]) for u in avail_utstyr]
    form.betalings_måte.choices = [(b[0], b[0]) for b in betalingsmåter]
    form.leveres_kunde.choices = [('Ja', 'Ja'), ('Nei','Nei')]

    if form.validate_on_submit():
        with Database() as db:
                
                betalingsmåte_id = db.get_betalingsmåte_id(form.betalings_måte.data)[0]
                utstyr_id,instans_id = form.avail_utstyr.data.split(".")

                db.add_utleie(current_user.id, form.kunde_nr.data, utstyr_id, instans_id, form.leveres_kunde.data, betalingsmåte_id, form.start_dato.data)
                return redirect(url_for('utleie.all'))
    return render_template('utleie/add_edit.html', form=form, utleie=None)

""" Registrere utleie
        *Velg kunde
        *Velg Utstyr(kun tilgjengelig)
        *Sett dato
        *Automatisk registrer hvilken ansatt som ekspederer

    Registrer innlevering
        *Marker utleie som levert
        *Sett innleveringsdato  """