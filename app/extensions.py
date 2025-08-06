from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from app.config.config import Config
from flask_socketio import SocketIO
app = Flask(
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="/static"
)
socketio = SocketIO(app, cors_allowed_origins="*")
app.config.from_object(Config)
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
mail = Mail(app)
r = FlaskRedis(app)
db = SQLAlchemy()
