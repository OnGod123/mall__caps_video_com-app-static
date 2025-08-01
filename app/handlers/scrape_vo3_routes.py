from flask import Blueprint
from app.handlers.login_routes import token_required 
from app.utils.pipe_line_v03 import scroll_to_bottom, skip_ads, try_get_transcript, run
from app.utils.index_transcript import index_results_in_elasticsearch
scrape_v03_bp = Blueprint('scrape_v03', __name__)
from playwright.sync_api import sync_playwright

@scrape_v03_bp.route('/scrape/version_0_3_mini', methods=['GET'])
@token_required
def scrape_v03(current_user):
    with sync_playwright() as playwright:
        results = run(playwright)
    index_results_in_elasticsearch(results)
    
