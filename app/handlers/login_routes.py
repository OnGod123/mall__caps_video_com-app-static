

from flask import Blueprint, request, jsonify, redirect, url_for, make_response, render_template
from datetime import datetime, timedelta
from functools import wraps
import jwt, json
from app.database.models import CreateUser
from app.database.database_engine import db
from flask_bcrypt import Bcrypt
from app.extensions import csrf
auth_bp = Blueprint('auth_bp', __name__)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = CreateUser.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated


@auth_bp.route('/login', methods=['GET'])
@csrf.exempt
def login():
    username = request.args.get('username')
    password = request.args.get('password')

    # First time visit (no username/password): render login page
    if not username or not password:
        return render_template('login.html')

    # Lookup user
    user = CreateUser.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        session['user_id'] = user.id

        # Redis session setup
        session_key = f"session:{user.id}"
        if not r.exists(session_key):
            r.setex(session_key, 3600, json.dumps({"urls": []}))

        # JWT token generation
        token = jwt.encode(
            {'user_id': user.id, 'exp': datetime.utcnow() + timedelta(hours=1)},
            app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        # Set JWT in cookie and redirect
        resp = make_response(redirect(url_for('profile')))
        resp.set_cookie('jwt', token)
        return resp

    return jsonify({'message': 'Invalid credentials'}), 401

