import pytest

from app import create_app
from store import NoteStore


@pytest.fixture()
def client():
    app = create_app(NoteStore())

    # Enable Flask testing mode.
    # Normally, Flask catches unhandled exceptions in routes and returns
    # a generic 500 Internal Server Error response.
    # With TESTING=True, Flask propagates those exceptions to the test client,
    # allowing pytest to show the actual error and traceback.
    app.config["TESTING"] = True
    # Create a test client to simulate HTTP requests without starting a server.
    return app.test_client()


def test_healthz(client):
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_notes_starts_empty(client):
    assert client.get("/notes").get_json() == []


def test_create_note_roundtrip(client):
    response = client.post("/notes", json={"title": "first", "body": "hello"})
    assert response.status_code == 201
    created = response.get_json()
    assert created["id"] == 1
    assert len(client.get("/notes").get_json()) == 1
    rv = client.get("/notes/1")
    assert rv.status_code == 200
    assert rv.get_json()["body"] == "hello"


def test_delete_note(client):
    note_id = client.post("/notes", json={"title": "gone"}).get_json()["id"]
    assert client.delete(f"/notes/{note_id}").status_code == 204
    assert client.get(f"/notes/{note_id}").status_code == 404


def test_create_note_requires_title(client):
    assert client.post("/notes", json={"body": "no title"}).status_code == 400


def test_non_json_body_rejected(client):
    rv = client.post("/notes", data="not json", content_type="text/plain")
    assert rv.status_code == 400


def test_get_missing_note_is_404(client):
    assert client.get("/notes/999").status_code == 404

# run pytest backend -v in the terminal
