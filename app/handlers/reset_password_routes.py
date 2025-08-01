from flask import Blueprint, render_template, request
from app.extensions import csrf
from datetime import datetime
from app.database.models import CreateUser, Reset
from app.extensions import db, bcrypt

reset_password_bp = Blueprint('reset_password_bp', __name__)

@reset_password_bp.route('/reset-password', methods=['POST', 'GET'])
@csrf.exempt
def reset_password():
    if request.method == 'GET':
        return render_template('reset_password.html')

    data = request.form
    reset_record = Reset.query.filter_by(reset_token=data['token']).first()

    if reset_record and reset_record.expires_at > datetime.utcnow():
        user = CreateUser.query.get(reset_record.user_id)
        user.password = bcrypt.generate_password_hash(data['new_password']).decode('utf-8')
        db.session.commit()

        return render_template('login.html', message='Password updated successfully, please log in.')

