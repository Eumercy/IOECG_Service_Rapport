from flask import Flask, jsonify, request
from flask_cors import CORS
from consul import register_service_with_consul,SERVICE_PORT



app = Flask(__name__)
CORS(app)


@app.route('/api/rapports/health')
def health():
    return jsonify({"status": "up"})        

@app.route('/api/rapports')
def test():
    return "Apk create"
if __name__ == "__main__":
    register_service_with_consul()
    app.run(debug=True,port=SERVICE_PORT)

    