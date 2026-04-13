from flask import render_template, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from database import Database
from models import Utstyr, FilterUtstyrForm

utstyr_bp = Blueprint('utstyr',__name__)

@utstyr_bp.route('/utstyr', methods=['GET', 'POST'])
@login_required
def all():
    
    form = FilterUtstyrForm()

    with Database() as db:
                
        utstyr_typer = db.get_utstyr_typer()
        kategorier = db.get_utstyr_kategorier()

        form.utstyr_type.choices = [('', 'Alle')] +[(t[0], t[0]) for t in utstyr_typer]
        form.kategori.choices = [('', 'Alle')] +[(k[0], k[0]) for k in kategorier]

        if form.validate_on_submit:
            utstyrer = [Utstyr(*utstyr) for utstyr in db.get_filtered_utstyr(
                        form.utstyr_type.data or None, 
                        form.kategori.data or None)]
        else:
            utstyrer = [Utstyr(*utstyr) for utstyr in db.get_all_utstyr()]

    return render_template('utstyr/read.html', form=form , utstyrer=utstyrer)