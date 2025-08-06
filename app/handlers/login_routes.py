
import logging 
from flask import session
from flask import Blueprint, request, jsonify, redirect, url_for, make_response, render_template, current_app
from datetime import datetime, timedelta
from functools import wraps
import jwt, json
from app.database.models import CreateUser
from app.database.database_engine import db
from app.extensions import csrf, bcrypt
from app.config.config import Config
from app.extensions import r    
auth_bp = Blueprint('auth_bp', __name__)
logger = logging.getLogger(__name__)

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
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = CreateUser.query.get(data['user_id'])
        except Exception:
            return jsonify({'message': 'please login to access this features!'}), 403

        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # If POST
    username = (request.form.get('username') or "").strip()
    password = request.form.get('password') or ""

    # Step 1: Missing input
    if not username or not password:
        logger.debug("[login] missing credentials: username=%r, password_present=%s", username, bool(password))
        return jsonify({'message': 'Invalid credentials (missing username or password)'}), 401

    # Step 2: Lookup user
    user = CreateUser.query.filter_by(username=username).first()
    if not user:
        logger.debug("[login] user not found for username=%r", username)
        return jsonify({'message': 'Invalid credentials (no such user)'}), 401

    # Step 3: Password verification
    password_ok = bcrypt.check_password_hash(user.password, password)
    logger.debug("[login] password check result for username=%r: %s", username, password_ok)
    if not password_ok:
        return jsonify({'message': 'Invalid credentials (bad password)'}), 401

    # Success path
    session['user_id'] = user.id

    # Redis session
    session_key = f"session:{user.id}"
    if not r.exists(session_key):
        r.setex(session_key, 3600, json.dumps({"urls": []}))

    # JWT token (needs current_app for config)
    token = jwt.encode(
        {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    resp = make_response(redirect(url_for('profile_view_bp.profile', identifier=user.id)))
    resp.set_cookie('jwt', token)
    return resp
