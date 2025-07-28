
from flask import Blueprint, render_template
from login_routes import token_required  # Adjust import path as needed

julia_bp = Blueprint('julia_bp', __name__)

@julia_bp.route('/julia')
@token_required
def render_julia(current_user):
    return render_template('julia.html', user=current_user)

