from flask import Blueprint
from decorators import token_required 
from app.utils.pipe_line_v03.py import scroll_to_bottom, skips_ads, try_get_transcript,run
from app.utils.index_transcript import index_results_in_elasticsearch
scrape_v03_bp = Blueprint('scrape_v03', __name__)

@scrape_v03_bp.route('/scrape/version_0_3_mini', methods=['GET'])
@token_required
def scrape_v03(current_user):
    results = run(playwright: Playwright)
    index_results_in_elasticsearch(results)
    
