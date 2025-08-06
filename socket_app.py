from flask import Flask, request
from flask import Blueprint, request, jsonify, redirect, url_for, make_response, render_template, current_app
from flask_socketio import SocketIO, Namespace, emit
import jwt
from Open_ai.analyze_with_openai import analyze_video_with_openai
from app.extensions import socketio
from app.utils.nlp_utils import extract_nlp_features
from app.config.config import Config
from elasticsearch_dsl import Search, Q
import traceback
INDEX_NAME = Config.INDEX_NAME
INDEX_NAME_2 = Config.INDEX_NAME_2

import traceback

class JuliaNamespace(Namespace):
    def on_connect(self):
        token = request.args.get("token") or request.cookies.get("jwt")
        if not token:
            print("No token provided")
            return False  # reject connection

        try:
            payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
            self.user_id = payload["user_id"]
            print(f"WebSocket connected: user {self.user_id}")
        except jwt.ExpiredSignatureError:
            print("JWT expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False
        except Exception as e:
            print("Unexpected error in on_connect:", e)
            traceback.print_exc()
            return False

    def on_message(self, data):
        print("on_message called with data:", data)

        if not isinstance(data, dict):
            emit("error", {"error": "Invalid data format"})
            return

        term = data.get("q", "").strip()
        print("Search term:", term)
        if not term:
            emit("error", {"error": "Empty search term"})
            return

        try:
            lemmas, entities = extract_nlp_features(term)
            print("Extracted NLP features:", lemmas, entities)
        except Exception as e:
            print("Error in extract_nlp_features:", e)
            traceback.print_exc()
            emit("error", {"error": f"NLP processing failed: {str(e)}"})
            return

        def search_in_index(index_name):
            print(f"Searching in index: {index_name}")
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
            print(f"Primary index returned {len(response)} hits")
            if not response.hits:
                raise ValueError("Empty result")
        except Exception as e:
            print("Primary index search failed:", e)
            traceback.print_exc()
            try:
                response = search_in_index(INDEX_NAME_2)
                print(f"Fallback index returned {len(response)} hits")
                if not response.hits:
                    emit("response", {"results": [], "message": "No results found in either index."})
                    return
            except Exception as e:
                print("Fallback search failed:", e)
                traceback.print_exc()
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
                print("AI analysis failed:", e)
                traceback.print_exc()
                ai_insight = {"error": f"AI analysis failed: {str(e)}"}

            results.append({
                "title": title,
                "url": hit.url,
                "score": hit.meta.score,
                "highlights": hit.meta.highlight.to_dict() if hasattr(hit.meta, "highlight") else {},
                "ai_insight": ai_insight
            })

        print("Emitting response with results:", results)
        emit("response", {
            "results": results,
            "message": "Search + AI insights complete."
        })




socketio.on_namespace(JuliaNamespace("/julia"))



