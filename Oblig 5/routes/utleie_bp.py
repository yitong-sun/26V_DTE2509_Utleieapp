from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utleie

utleie_bp = Blueprint('utleie',__name__)

@utleie_bp.route('/utleie')
@login_required
def all():
    with Database() as db:
        utstyrer = [Utleie(*utleie) for utleie in db.get_all_utleie()] #not implemented in Database yet

    return render_template('utleie/read.html', uteleier=utleier)

""" Registrere utleie
        *Velg kunde
        *Velg Utstyr(kun tilgjengelig)
        *Sett dato
        *Automatisk registrer hvilken ansatt som ekspederer

    Registrer innlevering
        *Marker utleie som levert
        *Sett innleveringsdato  """