from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config
from flask_cors import CORS

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    socketio.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app
