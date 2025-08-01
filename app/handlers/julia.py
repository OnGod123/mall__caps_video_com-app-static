
from flask import Blueprint, render_template
from app.handlers.login_routes import token_required  

julia_bp = Blueprint('julia_bp', __name__)

@julia_bp.route('/julia')
@token_required
def render_julia(current_user):
    return render_template('julia.html', user=current_user)

