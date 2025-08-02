from flask import Blueprint, render_template
from app.database.models import CreateUser
from app.database.database_engine import db
from app.handlers.login_routes import token_required

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

@admin_bp.route('/create', methods=['GET'])
@token_required
def create_admin(current_user=None):  # Accepts current_user but also works without it when exempt
    username = 'admin'
    password = 'supersecurepassword'

    existing = db.session.query(CreateUser).filter_by(username=username).first()
    if existing:
        message = f"Admin user '{username}' already exists."
    else:
        admin = CreateUser(username=username)
        admin.set_password(password)
        admin.is_admin = True
        db.session.add(admin)
        db.session.commit()
        message = f"Admin user '{username}' created successfully."

    return render_template('admin.html', message=message)

