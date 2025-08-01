from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from app.extensions import csrf
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_cors import CORS
from app.extensions import r, bcrypt
from flask_socketio import SocketIO
from socket_app import JuliaNamespace  # Correct import
from app.extensions import mail
from app.database.database_engine import db, init_elasticsearch,db_init_app
from app.database.models import CreateUser, Login, Profile, Reset, VideoDocument, Video_Document
from app.config.config import Config
import redis
app = Flask(__name__)
app.config.from_object('app.config.config.Config')

#extensions

bcrypt.init_app(app)
csrf.init_app(app)
mail.init_app(app)
r.init_app(app)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")
db_init_app(app)
init_elasticsearch()

with app.app_context():
    if not VideoDocument._index.exists():
        VideoDocument.init()
    db.create_all()

# === Import Blueprints ===
from app.handlers.Oauth_routes import auth_bp 
from app.handlers.login_routes import auth_bp as login
from app.handlers.forget_password_routes import forgot_password_bp
from app.handlers.logout_routes import logout_bp
from app.handlers.register_routes import register_bp
from app.handlers.reset_password_routes import reset_password_bp
from app.handlers.profile_routes import profile_bp as user_profile
from app.handlers.profile_updates_routes import profile_bp as profile_update_bp
from app.handlers.scrape_vo1_routes import scrape_v01_bp
from app.handlers.scrape_vo3_routes import scrape_v03_bp
from app.handlers.julia import julia_bp
from app.handlers.homes_routes import home_bp
from app.handlers.search_routes_01 import search_v01_bp
from app.handlers.search_routes_03 import search_v03_bp

# === Register Blueprints ===
app.register_blueprint(auth_bp)
app.register_blueprint(login)
app.register_blueprint(forgot_password_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(reset_password_bp)
app.register_blueprint(user_profile)
app.register_blueprint(profile_update_bp)
app.register_blueprint(search_v01_bp)
app.register_blueprint(search_v03_bp)
app.register_blueprint(scrape_v01_bp)
app.register_blueprint(scrape_v03_bp)
app.register_blueprint(julia_bp)
app.register_blueprint(home_bp)


# === Register WebSocket Namespace ===
socketio.on_namespace(JuliaNamespace("/julia"))

# === Entry Point ===
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=9000)

