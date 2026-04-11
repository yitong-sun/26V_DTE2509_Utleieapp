from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utstyr

utstyr_bp = Blueprint('utstyr',__name__)

@utstyr_bp.route('/utstyr')
@login_required
def all():
    with Database() as db:
        utstyrer = [Utstyr(*utstyr) for utstyr in db.get_all_utstyr()]

    return render_template('utstyr/read.html', utstyrer=utstyrer)