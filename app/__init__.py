from flask import Flask


from flask.ext.sqlalchemy import SQLAlchemy
from config import config
from flask.ext.login import LoginManager
from flask.ext.socketio import SocketIO

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
socketio = SocketIO()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    socketio.init_app(app)
    login_manager.init_app(app)
    db.init_app(app)

    from .chat import chat as chat_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(chat_blueprint, url_prefix='/chat')
    app.register_blueprint(auth_blueprint)

    return socketio.run(app)

