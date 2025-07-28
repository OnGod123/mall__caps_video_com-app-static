from flask import Flask, requestifrom flask_socketio import SocketIO, Namespace, emit
import jwt
from analyze_with_openai import analyze_video_with_openai
from Open_ai from analyze_video_with_openai
app = Flask(__name__)
app.config["SECRET_KEY"] = "your-secret"
socketio = SocketIO(app, cors_allowed_origins="*")

class JuliaNamespace(Namespace):
    def on_connect(self):
        token = request.args.get("token")
        try:
            payload = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            user_id = payload["user_id"]
            print(f"WebSocket connected: user {user_id}")
        except jwt.ExpiredSignatureError:
            print("JWT expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False

def on_message(self, data):
    if not isinstance(data, dict):
        emit("error", {"error": "Invalid data format"})
        return

    term = data.get("q", "").strip()
    if not term:
        emit("error", {"error": "Empty search term"})
        return

    try:
        lemmas, entities = extract_nlp_features(term)
    except Exception as e:
        emit("error", {"error": f"NLP processing failed: {str(e)}"})
        return

    def search_in_index(index_name):
        s = Search(index=index_name)
        should_queries = [
            Q("match", transcript={"query": term, "fuzziness": "AUTO", "operator": "and"}),
            Q("match_phrase", transcript={"query": term, "slop": 2}),
            Q("match", title={"query": term, "boost": 2.0, "fuzziness": "AUTO"}),
            Q("match", multi_title={"query": term, "boost": 2.5}),
        ]

        for lemma in lemmas:
            should_queries.extend([
                Q("match", transcript={"query": lemma, "boost": 1.5}),
                Q("match", multi_title={"query": lemma, "boost": 2.0})
            ])
        for entity in entities:
            should_queries.extend([
                Q("match_phrase", transcript={"query": entity, "boost": 2.0}),
                Q("term", multi_title={"value": entity.lower(), "boost": 3.0})
            ])

        s = s.query(Q("bool", should=should_queries, minimum_should_match=1))
        s = s.highlight("transcript", "title")
        return s.execute()

    # Try primary index, fallback to secondary
    try:
        response = search_in_index(INDEX_NAME)
        if not response.hits:
            raise ValueError("Empty result")
    except Exception:
        try:
            response = search_in_index(INDEX_NAME_2)
            if not response.hits:
                emit("response", {"results": [], "message": "No results found in either index."})
                return
        except Exception as e:
            emit("error", {"error": f"Fallback search failed: {str(e)}"})
            return

    results = []
    for hit in response:
        title = hit.title
        transcript = ""
        if hasattr(hit.meta.highlight, "transcript"):
            transcript = hit.meta.highlight.transcript[0]

        try:
            ai_insight = analyze_video_with_openai(title, transcript)
        except Exception as e:
            ai_insight = {"error": f"AI analysis failed: {str(e)}"}

        results.append({
            "title": title,
            "url": hit.url,
            "score": hit.meta.score,
            "highlights": hit.meta.highlight.to_dict() if hasattr(hit.meta, "highlight") else {},
            "ai_insight": ai_insight
        })

    emit("response", {
        "results": results,
        "message": "Search + AI insights complete."
    })


socketio.on_namespace(JuliaNamespace("/julia"))



