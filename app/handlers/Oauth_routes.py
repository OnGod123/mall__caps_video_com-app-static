from flask import Blueprint, request, redirect, session, url_for, jsonify, current_app
from app.database.database_engine import db
from app.database.models import CreateUser
from authlib.integrations.flask_client import OAuth
import uuid
import os

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

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/Google/login")
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    user_info = google.get("userinfo").json()
    user_email = user_info.get("email")

    if not user_email:
        return jsonify({"error": "Failed to get user email"}), 400

    user = CreateUser.query.filter_by(gmail=user_email).first()

    if not user:
        user = CreateUser(
            name=user_info.get("name"),
            username=user_info.get("name"),
            gmail=user_email,
            password="",  # leave blank or use default
        )
        db.session.add(user)
        db.session.commit()

    session["user_email"] = user_email
    return redirect("/profile")




