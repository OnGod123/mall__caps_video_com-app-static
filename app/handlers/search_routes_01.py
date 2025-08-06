from flask import Blueprint, request, render_template, jsonify
from elasticsearch_dsl import Search, Q
from app.utils.nlp_utils import extract_nlp_features
from app.config.config import Config
from app.handlers.login_routes import token_required
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

index_name = Config.INDEX_NAME
index_name_2 = Config.INDEX_NAME_2

search_v01_bp = Blueprint('search_bp', __name__)

@search_v01_bp.route("/search/version_01", methods=["GET"])
@token_required
def search(current_user):
    term = request.args.get("query", " ").strip()
    logger.debug(f"[search_v01] Search term: '{term}' from user_id={current_user.id}")
    print(f"[search_v01] Search term: '{term}' from user_id={current_user.id}")

    if not term:
        logger.debug("[search_v01] No term provided — rendering template")
        print("[search_v01] No term provided — rendering template")
        return render_template("search_01.html")

    # NLP processing
    lemmas, entities = extract_nlp_features(term)
    logger.debug(f"[search_v01] Extracted lemmas: {lemmas}, entities: {entities}")
    print(f"[search_v01] Extracted lemmas: {lemmas}, entities: {entities}")

    s = Search(index=index_name_2)

    should_queries = [
        Q("match", transcript={"query": term, "fuzziness": "AUTO", "operator": "and"}),
        Q("match_phrase", transcript={"query": term, "slop": 2}),
        Q("match", title={"query": term, "boost": 2.0, "fuzziness": "AUTO"}),
        Q("match", multi_title={"query": term, "boost": 2.5}),
    ]

    for lemma in lemmas:
        should_queries.append(Q("match", transcript={"query": lemma, "boost": 1.5}))
        should_queries.append(Q("match", multi_title={"query": lemma, "boost": 2.0}))

    for entity in entities:
        should_queries.append(Q("match_phrase", transcript={"query": entity, "boost": 2.0}))
        should_queries.append(Q("term", multi_title={"value": entity.lower(), "boost": 3.0}))

    s = s.query(Q("bool", should=should_queries, minimum_should_match=1))
    s = s.highlight("transcript", "title")

    try:
        response = s.execute()
        logger.debug(f"[search_v01] ES returned {len(response)} hits")
        print(f"[search_v01] ES returned {len(response)} hits")
        if len(response) == 0:
            print("[search_v01] No data fetched from Elasticsearch")
    except Exception as e:
        logger.exception("[search_v01] Elasticsearch query failed")
        print(f"[search_v01] Elasticsearch query failed: {e}")
        return jsonify({"error": str(e)}), 500

    results = [{
        "title": hit.title,
        "url": hit.url,
        "highlights": hit.meta.highlight.to_dict() if hasattr(hit.meta, "highlight") else {},
        "score": hit.meta.score
    } for hit in response]

    logger.debug(f"[search_v01] Final results: {results}")
    print(f"[search_v01] Final results: {results}")

    return jsonify(results)

