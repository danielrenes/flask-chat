from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO

import eventlet
eventlet.monkey_patch()

db = SQLAlchemy()
socketio = SocketIO()

from . import models
import notifications

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    socketio.init_app(app)

    from .blueprints import ui, usr, msg
    app.register_blueprint(ui)
    app.register_blueprint(usr)
    app.register_blueprint(msg)

    return app
