from flask import Flask, render_template
from flask_login import login_required
from flask_wtf import CSRFProtect
import secrets
from database import Database
from models import Utleie

from routes.user_manager import users_bp, login_manager
from routes.utstyr_bp import utstyr_bp
from routes.utleie_bp import utleie_bp
from routes.kunder_bp import kunder_bp
from routes.statistikk_bp import statistikk_bp


app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
csrf = CSRFProtect(app)

login_manager.init_app(app)


#Blueprints 
app.register_blueprint(users_bp, url_prefix = '/users')
app.register_blueprint(utstyr_bp, url_prefix = '/utstyr')
app.register_blueprint(utleie_bp, url_prefix = '/utleie')
app.register_blueprint(kunder_bp, url_prefix = '/kunder')
app.register_blueprint(statistikk_bp, url_prefix = '/statistikk')


@app.route("/")
@login_required
def home():
    with Database() as db:
        
        #Oversikt

        #Antall aktive utleier
        if db.get_total_antall_aktiv_utleie() != None:
            antall_aktive_utleie = db.get_total_antall_aktiv_utleie()[0]
        else:
            antall_aktive_utleie = 0

        #Antall tilgjengilige utstyr
        if db.get_antall_tilgjengelinge_utstyr() != None:
            antall_tilgjengelige_utstyr = db.get_antall_tilgjengelinge_utstyr()[0]
        else:
            antall_tilgjengelige_utstyr = 0

        #Fem siste utleier
        utleier = [Utleie(*utleie) for utleie in db.get_fem_siste_utleier()]

    return render_template("index.html",
                           #variabler: 
                            antall_aktive_utleie=antall_aktive_utleie,
                            antall_tilgjengelige_utstyr=antall_tilgjengelige_utstyr,
                            utleier = utleier                               
                            )


if __name__ == "__main__":
    app.run(debug=True, port=8000)