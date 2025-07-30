from flask import Blueprint, session, make_response, render_template
from main import r
from app.handlers.auth_helpers import token_required  # Adjust import path as needed

logout_bp = Blueprint('logout_bp', __name__)

@logout_bp.route('/logout', methods=['POST', 'GET'])
@token_required
def logout(current_user):
    session.pop('user_id', None)
    r.delete(f"session:{current_user.id}")

    resp = make_response(render_template('logout.html', message='You have been logged out.'))
    resp.set_cookie('jwt', '', expires=0)
    return resp
