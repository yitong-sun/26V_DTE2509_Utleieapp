from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required
from flask_wtf import CSRFProtect
import secrets

from routes.user_manager import users_bp, login_manager
from routes.utstyr_bp import utstyr_bp
#remove hash when implemented
#from routes.utleie_bp import utleie_bp 
#from routes.kunder_bp import kunder_bp
from routes.statistikk_bp import statistikk_bp

#must remember to add CSRFProtect for WTF

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
csrf = CSRFProtect(app)

login_manager.init_app(app)


#Blueprints 
# remove hash when implemented
app.register_blueprint(users_bp, url_prefix = '/users')
app.register_blueprint(utstyr_bp, url_prefix = '/utstyr')
#app.register_blueprint(utleie_bp, url_prefix = '/utstyr')
#app.register_blueprint(kunder_bp, url_prefix = '/kunder')
app.register_blueprint(statistikk_bp, url_prefix = '/statistikk')


@app.route("/")
@login_required
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)