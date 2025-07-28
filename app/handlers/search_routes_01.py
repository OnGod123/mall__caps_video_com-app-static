from flask import Blueprint, request, render_template, jsonify
from elasticsearch_dsl import Search, Q
from utils.nlp_utils import extract_nlp_features
from config import INDEX_NAME, INDEX_NAME_2
from login_routes import token_required

search_bp = Blueprint('search_bp', __name__)
@search_bp.route("/search/version_01", methods=["GET"])
@token_required
def search(current_user):
    term = request.args.get("q", "").strip()

    if not term:
        return render_template("search.html")

    lemmas, entities = extract_nlp_features(term)
    s = Search(index=INDEX_NAME_2)

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
    response = s.execute()

    return jsonify([{
        "title": hit.title,
        "url": hit.url,
        "highlights": hit.meta.highlight.to_dict() if hasattr(hit.meta, "highlight") else {},
        "score": hit.meta.score
    } for hit in response])
