from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis

bcrypt = Bcrypt()
csrf = CSRFProtect()
mail = Mail()
db = SQLAlchemy()
r = FlaskRedis()

