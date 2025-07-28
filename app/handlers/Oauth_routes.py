from flask import Blueprint, request, redirect, session, url_for, jsonify
from models.models import User
from app 
import uuid

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID", "your-google-client-id"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET", "your-google-client-secret"),
    access_token_url='https://oauth2.googleapis.com/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params={
        "access_type": "offline",
        "prompt": "consent"
    },
    api_base_url='https://www.googleapis.com/oauth2/v2/',
    userinfo_endpoint='https://www.googleapis.com/oauth2/v2/userinfo',
    client_kwargs={'scope': 'openid email profile'}
)


auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login")
def login():
    redirect_uri = url_for("auth.auth_callback", _external=True)
    return google.authorize_redirect(redirect_uri)

@auth_bp.route("/auth/callback")
def auth_callback():
    token = google.authorize_access_token()
    user_info = google.parse_id_token(token)
    user_email = user_info.get("email")

    if not user_email:
        return jsonify({"error": "Failed to get user email"}), 400

    user = db.users.find_one({"email": user_email})

    if not user:
        user = {
            "_id": str(uuid.uuid4()),
            "email": user_email,
        }
        db.users.insert_one(user)

    session["user_email"] = user_email
    return redirect("/profile")



