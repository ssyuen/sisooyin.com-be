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

def test_add_watched_episode(client):    
    response = client.post(
        "/api/one_piece/watched/add",
        json={            
            "episode_id": 1,
            "watched_date": "2022-01-01",
            "workout_id": 1
        }
    )
    assert response.status_code == 200

    client.delete("/api/one_piece/watched/1&1")
    assert response.status_code == 200


def test_get_and_delete_watched_episode(client):
    # Insert test watched episode first
    watched_episode_data = {
        "episode_id": 100,
        "watched_date": "2022-01-01",
        "workout_id": 100
    }
    response = client.post("/api/one_piece/watched/add", json=watched_episode_data)
    assert response.status_code == 200


    response = client.get(f"/api/one_piece/watched/{watched_episode_data['episode_id']}&{watched_episode_data['workout_id']}")
    assert response.status_code == 200

    response = client.delete(f"/api/one_piece/watched/{watched_episode_data['episode_id']}&{watched_episode_data['workout_id']}")
    assert response.status_code == 200

    response = client.get(f"/api/one_piece/watched/{watched_episode_data['episode_id']}&{watched_episode_data['workout_id']}")
    assert response.status_code == 404
