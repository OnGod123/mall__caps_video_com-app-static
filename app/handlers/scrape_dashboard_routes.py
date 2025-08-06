from flask import Blueprint, render_template
from app.handlers.login_routes import token_required

scrape_dashboard_bp = Blueprint('scrape_dashboard', __name__)

@scrape_dashboard_bp.route('/scrape/dashboard', methods=['GET'])
@token_required
def scrape_dashboard(current_user):
    return render_template('scrape_dashboard.html', user=current_user)

