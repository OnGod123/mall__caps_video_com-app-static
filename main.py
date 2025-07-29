from flask import Flask
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_cors import CORS
from flask_socketio import SocketIO
from socket_app import JuliaNamespace  # Correct import
from app.database.database_engine import db, init_elasticsearch
from app.database.models import CreateUser, Login, Profile, Reset, Videodocument, Video_Document

app = Flask(__name__)
app.config.from_object('config.Config')

# Extensions
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
mail = Mail(app)
r = FlaskRedis(app)

CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

db_init_app(app)
init_elasticsearch()
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)




@app.before_first_request
def create_tables():
    Base.metadata.create_all(bind=engine)

# === Import Blueprints ===
from handlers.auth_routes import auth_bp
from app.handlers.forgot_password_routes import forgot_password_bp
from app.handlers.logout_routes import logout_bp
from app.handlers.register_routes import register_bp
from app.handlers.reset_password_routes import reset_password_bp
from app.handlers.profile_routes import profile_bp as profile_view_bp
from app.handlers.update_profile_routes import profile_bp as profile_update_bp
from app.handlers.search_routes import search_bp
from app.handlers.scrape_v01_routes import scrape_v01_bp
from app.handlers.scrape_v03_routes import scrape_v03_bp
from app.handlers.julia_routes import julia_bp
from app.handlers.home_routes import home_bp
from app.handlers.search_v01_routes import search_v01_bp
from app.handlers.search_v03_routes import search_v03_bp

# === Register Blueprints ===
app.register_blueprint(auth_bp)
app.register_blueprint(forgot_password_bp)
app.register_blueprint(logout_bp)
app.register_blueprint(register_bp)
app.register_blueprint(reset_password_bp)
app.register_blueprint(profile_view_bp)
app.register_blueprint(profile_update_bp)
app.register_blueprint(search_bp)
app.register_blueprint(scrape_v01_bp)
app.register_blueprint(scrape_v03_bp)
app.register_blueprint(julia_bp)
app.register_blueprint(home_bp)
app.register_blueprint(search_v01_bp)
app.register_blueprint(search_v03_bp)

# === Register WebSocket Namespace ===
socketio.on_namespace(JuliaNamespace("/julia"))

# === Entry Point ===
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=9000)

