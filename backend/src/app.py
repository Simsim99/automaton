import os
from flask import Flask, jsonify, request
# jsonify converts Python dicts to a proper JSON response
from store import NoteStore
from sqlstore import SqlStore


# function that creates a flask object if store is None otherwise build a
# fresh NoteStore
def create_app(store: NoteStore | None = None) -> Flask:
    app = Flask(__name__)
    # # Tell Flask which Python module contains the application, so it can
    # locate resources like templates and static files.
    if store is None:
        if "DB_HOST" in os.environ:
            store = SqlStore()
        else:
            store = NoteStore()

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok"), 200

    @app.get("/notes")
    def get_notes():
        return jsonify(store.all()), 200

    @app.post("/notes")
    def post_notes():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify(error="body must be JSON"), 400
        title = data.get("title")
        body = data.get("body", "")
        if not isinstance(title, str) or title.strip() == "":
            return jsonify(
                error="title is required and must be non-empty"), 400
        if not isinstance(body, str):
            return jsonify(error="body must be a string"), 400
        note = store.add(title.strip(), body)
        return jsonify(note), 201

    @app.get("/notes/<int:note_id>")
    def get_a_note(note_id):
        note = store.get(note_id)
        if note is None:
            return jsonify(error="note not found"), 404
        return jsonify(note), 200

    @app.delete("/notes/<int:note_id>")
    def del_a_note(note_id):
        if not store.delete(note_id):
            return jsonify(error="note not found"), 404
        return "", 204
    return app


if __name__ == "__main__":
    app = create_app(NoteStore())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
