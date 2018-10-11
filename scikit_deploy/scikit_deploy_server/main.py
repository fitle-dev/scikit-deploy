from flask import Flask
from flask_cors import CORS
from server.scoring import app_blueprint

SERVER_PORT = 5000

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)
    CORS(app)

    app.run(host='0.0.0.0', port=SERVER_PORT, debug=True)
