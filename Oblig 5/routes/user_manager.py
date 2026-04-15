from flask import render_template, redirect, url_for, request, Blueprint, jsonify
from flask_login import logout_user, login_required, login_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from database import Database
from models import User

users_bp = Blueprint('users',__name__)
login_manager = LoginManager()
login_manager.login_view = 'users.login'

@login_manager.user_loader
def load_user(user_id):
    with Database() as db:
        user = db.load_user(user_id)
        if user:
            return User(user[0], user[1], user[2], user[3], user[5])
        return None

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        kundeb_id = request.form['id']
        fornavn = request.form['fornavn']
        etternavn = request.form['etternavn']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        with Database() as db:
            if db.check_id_in_use(kundeb_id)[0] == True:
                return render_template('users/register.html', error = "ID allerede i bruk")
            else:
                db.create_user(kundeb_id, fornavn, etternavn, email, password)
                db.create_kundebehandler(kundeb_id,fornavn, etternavn)
            return redirect( url_for('users.login'), error="Ny konto registrert" )
    return render_template("users/register.html")

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        with Database() as db:
            user = db.load_user_by_email(email)

            if user and check_password_hash(user[4], password):
                login_user(User(user[0], user[1], user[2], user[3], user[5]))
                return redirect( url_for('home'))
            
        return render_template('users/login.html', error = "Feil e-post eller passord")
    return render_template("users/login.html")

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for("users.login"))

@users_bp.route('/profile')
@login_required
def profile():
    return render_template("users/profile.html", user = current_user)

@users_bp.route('/check_id')
def check_id():
    user_id = request.args.get('user_id')

    with Database() as db:
        user = db.check_id_in_use(user_id)[0]

    return jsonify({'exists': bool(user)})
     