from flask import Flask
from server.scoring import app_blueprint
import os

SERVER_PORT = int(os.environ.get('SERVER_PORT', 5000))


def get_app():
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)
    return app


app = get_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=SERVER_PORT, debug=True)
