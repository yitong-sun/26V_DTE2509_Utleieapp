from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Kunde

kunde_bp = Blueprint('kunde',__name__)

@kunde_bp.route('/kunde')
@login_required
def all():
    with Database() as db:
        utstyrer = [Kunde(*kunde) for kunde in db.get_all_kunde()] #not implemented properly in Database.py yet

    return render_template('kunder/read.html', kunder=kunder)