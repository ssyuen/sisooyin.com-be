import pytest
import sys
import os

# Add the parent directories to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import the app module
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_and_delete_episode_by_id(client):
    # Insert test episode first
    episode_data = {
        "id": 1,
        "title": "Episode 1",
        "description": "The beginning of the adventure",
        "saga_id": 2
    }
    response = client.post("/api/one_piece/episode/add", json=episode_data)
    assert response.status_code == 200

    response = client.get("/api/one_piece/episode/1")
    assert response.status_code == 200

    response = client.delete("/api/one_piece/episode/delete/1")
    assert response.status_code == 200
    
    response = client.get("/api/one_piece/episode/1")
    assert response.status_code == 404