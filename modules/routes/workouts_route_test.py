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

def test_get_workouts(client):
    response = client.get("/api/workouts")
    assert response.status_code == 200
