from flask import Blueprint
from decorators import token_required
from app.utils.pipe_line_v01.py import scrape_transcripts
from app.utils.index_transcript import index_results_in_elasticsearch 
scrape_v01_bp = Blueprint('scrape_v01', __name__)

@scrape_v01_bp.route('/scrape/version_0_1_mini', methods=['GET'])
@token_required
def scrape_v01(current_user):
    result = scrape_transcripts(channel_url="https://www.youtube.com/@MrBeastGaming/videos", max_videos=100, max_attempts=4)
     index_results_in_elasticsearch(result)
