from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utstyr_Inntekt, Utleie_Aktiv, Utstyr_Antall_Utleid

statistikk_bp = Blueprint('statistikk',__name__, url_prefix='/statistikk')



@statistikk_bp.route('/')
@login_required
def all_statistikk():
    with Database() as db:

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
                           utstyrer=utstyrer, 
                           antall_komplette_utleier=antall_komplette_utleier,
                           aktive_utleier= aktive_utleier,
                           kundebehandler_navn= kundebehandler_navn,
                           flest_utleid_utstyrer=flest_utleid_utstyrer,
                           flest_antall=flest_antall)


