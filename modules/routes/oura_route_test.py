import pytest
import sys
import os
from datetime import datetime, timedelta

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
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    response = client.get(f"/api/workouts?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200

def test_get_sleep(client):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    response = client.get(f"/api/sleep?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200

def test_get_activity(client):
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    response = client.get(f"/api/activity?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200