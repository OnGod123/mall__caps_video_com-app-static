from flask import Blueprint, render_template, request
from flask_wtf.csrf import CSRFProtect
from flask_mail import Message
from datetime import datetime, timedelta
import secrets
from app.database.models import CreateUser, Reset
from app.handlers.login_routes import token_required
from app.extensions import csrf

forgot_password_bp = Blueprint('forgot_password_bp', __name__)
csrf_protect = CSRFProtect()

@forgot_password_bp.route('/forgot-password', methods=['GET', 'POST'])
@token_required
@csrf.exempt
def forgot_password(current_user):
    if request.method == 'GET':
        return render_template('forgot_password.html')

    data = request.form
    user = CreateUser.query.filter_by(gmail=data['gmail']).first()
    if user:
        reset_token = secrets.token_urlsafe(16)
        expires = datetime.utcnow() + timedelta(minutes=10)
        db.session.add(Reset(user_id=user.id, reset_token=reset_token, expires_at=expires))
        db.session.commit()

        msg = Message('Password Reset Code', sender='noreply@mallcaps.com', recipients=[user.gmail])
        msg.html = f"<h1>Password Reset Code</h1><p>{reset_token}</p>"
        mail.send(msg)

        return render_template('reset_password.html', gmail=user.gmail, message='Reset code sent to your email.')

    return render_template('forgot_password.html', error='Email not found')

