
from flask import Blueprint, request, jsonify, redirect, url_for, make_response, render_template
from datetime import datetime, timedelta
from functools import wraps
import jwt, json
from app.database.models import CreateUser
from app.database.database_engine import db
from flask_bcrypt import Bcrypt
from app.extensions import csrf
from app.config.config import Config
  
auth_bp = Blueprint('auth_bp', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Skip auth for exempt routes
        if request.endpoint in Config.TOKEN_EXEMPT_ROUTES:
            return f(*args, **kwargs)

        token = request.cookies.get('jwt')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, Config.SECRET_KEY['SECRET_KEY'], algorithms=["HS256"])
            current_user = CreateUser.query.get(data['user_id'])
        except Exception:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # If POST
    username = request.form.get('username')
    password = request.form.get('password')

    user = CreateUser.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id

        # Redis session
        session_key = f"session:{user.id}"
        if not r.exists(session_key):
            r.setex(session_key, 3600, json.dumps({"urls": []}))

        # JWT token
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        # Set cookie and redirect
        resp = make_response(redirect(url_for('profile_view_bp.profile', identifier=user.id)))
        resp.set_cookie('jwt', token)
        return resp

    return jsonify({'message': 'Invalid credentials'}), 401


