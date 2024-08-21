from flask import Flask
from routes.home import home_route
from routes.Cad_Eqto import Cad_Eqto_route

app = Flask(__name__)

app.register_blueprint(home_route)
app.register_blueprint(Cad_Eqto_route, url_prefix="/Cad_Eqto")

app.run(debug=True)
