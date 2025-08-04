from flask import Blueprint, request, render_template, jsonify
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from app.extensions import db, bcrypt, mail
from app.database.models import CreateUser
from app.extensions import csrf
from app.extensions import db
from app.database.models import Profile
from app.handlers.profile_for_user import create_profile_for_user


register_bp = Blueprint('register_bp', __name__)

@register_bp.route('/register', methods=['GET', 'POST'])
@csrf.exempt
def register():
    if request.method == 'GET':
        return render_template('register.html')  # Your HTML form here

    data = request.form

    # Basic validation
    if not all([data.get('name'), data.get('username'), data.get('password'), data.get('gmail')]):
        return jsonify({'error': 'Missing fields'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user = CreateUser(
        name=data['name'],
        username=data['username'],
        password=hashed_password,
        gmail=data['gmail']
    )
    db.session.add(user)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email registered'}), 409

    # ✅ NOW we create the profile (user.id exists)
    create_profile_for_user(user)

    # Send welcome email
    msg = Message(
        subject='Welcome!',
        sender='noreply@mallcaps.com',
        recipients=[data['gmail']]
    )
    msg.html = f"""
        <h1>Welcome {data['name']}!</h1>
        <p>Your username is: <strong>{data['username']}</strong></p>
        <p>Thanks for joining MallCaps!</p>
    """
    mail.send(msg)

    return render_template('registration_success.html', name=data['name'])

