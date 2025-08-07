import time
from flask import Blueprint
from app.handlers.login_routes import token_required
from app.utils.pipe_line_v01 import scrape_transcripts
from app.utils.index_transcript import index_results_in_elasticsearch 
scrape_v01_bp = Blueprint('scrape_v01', __name__)

@scrape_v01_bp.route('/scrape/version_0_1_mini', methods=['GET'])
@token_required
def scrape_v01(current_user):
    start_time = time.time()
    try:
        result = scrape_transcripts(
            channel_url="https://www.youtube.com/@MrBeastGaming/videos",
            max_videos=500,
            max_attempts=4
        )
        index_results_in_elasticsearch(result)
        return jsonify({"status": "success", "message": "Scraping v0.1 completed successfully!"}), 200
    except Exception as e:
        elapsed = time.time() - start_time
        if elapsed >= 180:  # 3 minutes
            return jsonify({"status": "error", "message": "Your network bandwidth is slow, please try again later."}), 408
        else:
            return jsonify({"status": "error", "message": str(e)}), 500
