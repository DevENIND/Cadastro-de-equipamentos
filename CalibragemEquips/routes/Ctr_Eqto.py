from flask import Blueprint, render_template
from database.equipamentos import lista_equipamentos

Ctr_Eqto_route = Blueprint('Ctr_Eqto', __name__)

@Ctr_Eqto_route.route('/')
def lista_eqtos():
    #Lista os equipamentos
    return render_template('Ctr_Eqto.html', equipamentos=lista_equipamentos)
