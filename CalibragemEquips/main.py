from flask import Flask
from jinja2.utils import F
from routes.log_eqto import log_eqto_route
from routes.Cad_Eqto import Cad_Eqto_route
from routes.Ctr_Eqto import Ctr_Eqto_route

app = Flask(__name__)

app.register_blueprint(log_eqto_route, url_prefix="/log_eqto")
app.register_blueprint(Cad_Eqto_route, url_prefix="/Cad_Eqto")
app.register_blueprint(Ctr_Eqto_route, url_prefix="/Ctr_Eqto")

app.run(debug=True)
