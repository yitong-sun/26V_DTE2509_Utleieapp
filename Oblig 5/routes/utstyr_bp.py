from flask import render_template, Blueprint
from flask_login import login_required
from database import Database
from models import Utstyr, FilterUtstyrForm, Instans

utstyr_bp = Blueprint('utstyr',__name__)

@utstyr_bp.route('/', methods=['GET', 'POST'])
@login_required
def all():
    
    form = FilterUtstyrForm()

    with Database() as db:

        tilgjengelig =[]
        for utstyr_instans_id in db.get_utstyr_instans_id():
                if db.check_status_utstyr_instans_id(utstyr_instans_id[0]):
                    print(utstyr_instans_id[0], "Yes")
                    tilgjengelig.append(utstyr_instans_id[0])
                else:
                     print(utstyr_instans_id[0], "No")

        utstyr_typer = db.get_utstyr_typer()
        kategorier = db.get_utstyr_kategorier()

        form.utstyr_type.choices = [('', 'Alle')] +[(t[0], t[0]) for t in utstyr_typer]
        form.kategori.choices = [('', 'Alle')] +[(k[0], k[0]) for k in kategorier]

        if form.validate_on_submit():
            utstyrer = [Utstyr(*utstyr) for utstyr in db.get_filtered_utstyr(
                        form.utstyr_type.data or None, 
                        form.kategori.data or None)]
            
        else:
            utstyrer = [Utstyr(*utstyr) for utstyr in db.get_all_utstyr()]

        instanser = [Instans(*instans) for instans in db.get_all_instans()]



    return render_template('utstyr/read.html', 
                           form=form , 
                           utstyrer=utstyrer, 
                           tilgjengelig=tilgjengelig,
                           instanser=instanser
                           )