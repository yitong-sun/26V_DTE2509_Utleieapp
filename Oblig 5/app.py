from flask import Flask, render_template, redirect, url_for, request
from flask_login import login_required
from routes.user_manager import users_bp, login_manager
from routes.utstyr_bp import utstyr_bp
#remove hash when implemented
#from routes.utleie_bp import utleie_bp 
#from routes.kunder_bp import kunder_bp
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)
login_manager.init_app(app)


#Blueprints 
# remove hash when implemented
app.register_blueprint(users_bp, url_prefix = '/users')
app.register_blueprint(utstyr_bp, url_prefix = '/utstyr')
#app.register_blueprint(utleie_bp, url_prefix = '/utstyr')
#app.register_blueprint(kunder_bp, url_prefix = '/kunder')

@app.route("/")
@login_required
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, port=8000)