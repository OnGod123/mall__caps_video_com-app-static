from flask import Blueprint, request, redirect, session, url_for, jsonify, current_app, make_response
from app.database.database_engine import db
from app.database.models import CreateUser
from authlib.integrations.flask_client import OAuth
import jwt
from datetime import datetime, timedelta
import os

auth_bp = Blueprint('auth', __name__)

oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "your-google-client-id"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "your-google-client-secret"),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)

@auth_bp.route("/Google/login")
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    redirect_uri = redirect_uri.replace("127.0.0.1", "localhost")
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/auth/callback")
def auth_callback():
    # Step 1: Exchange code for token
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    user_email = user_info.get("email")

    if not user_email:
        return jsonify({"error": "Failed to get user email"}), 400

    # Step 2: Check or create user
    user = CreateUser.query.filter_by(gmail=user_email).first()
    if not user:
        user = CreateUser(
            name=user_info.get("name"),
            username=user_info.get("name"),
            gmail=user_email,
            password=""  # No password for OAuth users
        )
        db.session.add(user)
        db.session.commit()

    # Step 3: Generate JWT
    jwt_token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.utcnow() + timedelta(hours=2)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    # Step 4: Store JWT in cookie
    resp = make_response(redirect(f"/profile/{user.id}"))
    resp.set_cookie(
        "jwt",
        jwt_token,
        httponly=True,
        samesite="Lax",
        secure=False  # True if HTTPS
    )

    return resp

