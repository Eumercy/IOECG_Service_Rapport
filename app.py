from flask import Flask, jsonify, request
from flask_cors import CORS
from database import db
from config.config import Config
from consul import register_service_with_consul 



app = Flask(__name__)
CORS(app)
# configuration de la base de donnée
app.config.from_object(Config)
db.init_app(app)


from api import deleteRapportById, getAllRapports, getRapportById, health, createRapport, get_rapports_for_analysis

#les routes
app.route('/api/rapports/health')(health)
app.route('/api/rapports/<int:id_experience>',methods=['POST'])(createRapport)
app.route('/api/rapports/<int:id_analyse>', methods=['GET'])(get_rapports_for_analysis)

app.route('/api/rapports/delete/<int:id>', methods=["DELETE"])(deleteRapportById)
app.route('/api/rapports/allRapport', methods=['GET'])(getAllRapports)
app.route('/api/rapports/<int:id>', methods=["GET"])(getRapportById)


if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True,port=Config.SERVICE_PORT)

    