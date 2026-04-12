from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Kunde, Utstyr, Utleie, Utstyr_Inntekt, Utleie_Aktiv

statistikk_bp = Blueprint('statistikk',__name__, url_prefix='/statistikk')



@statistikk_bp.route('/')
@login_required
def all_statistikk():
    with Database() as db:

        #B aktive utleier
        aktive_utleier = [Utleie_Aktiv(*utleie) for utleie in db.aktive_utleier(current_user.id)]
        #C Komplette utleier
        antall_komplette_utleier = db.komplette_utleier()[0]
        #D Innetkt per utstyr
        utstyrer = [Utstyr_Inntekt(*utstyr) for utstyr in db.tjent_per_utstyr()]


    return render_template('Statistikk/read.html',
                           #variabler: 
                           utstyrer=utstyrer, 
                           antall_komplette_utleier=antall_komplette_utleier,
                           aktive_utleier= aktive_utleier)


