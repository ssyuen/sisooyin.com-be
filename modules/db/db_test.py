import pytest
import os
from client import Client
from utils import get_daily_db_file

@pytest.fixture(scope="module")
def db_client():
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    
    # Create tables
    client.query("CREATE TABLE IF NOT EXISTS episode (id INTEGER PRIMARY KEY, title TEXT, description TEXT, saga_id INTEGER)")
    client.query("CREATE TABLE IF NOT EXISTS watched_episode (episode_id INTEGER, workout_id INTEGER, watched_date TEXT)")
    client.query("CREATE TABLE IF NOT EXISTS saga (id INTEGER PRIMARY KEY, title TEXT, saga_episode_start INTEGER, saga_episode_end INTEGER)")
    client.query("CREATE TABLE IF NOT EXISTS workout (id INTEGER PRIMARY KEY, distance INTEGER, work FLOAT, date TEXT)")

    yield client

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_saga_without_escape_characters(db_client):
    # Example saga data
    saga_data = {
        "id": 2,
        "title": "Alabasta",
        "saga_number": "2",
        "saga_chapitre": "101 à 216",
        "saga_volume": "12 à 23",
        "saga_episode": "62 à 143"
    }

    # Parse the saga_episode
    saga_episode_start, saga_episode_end = parse_saga_episode(saga_data["saga_episode"])

    # Insert the saga data into the saga table
    db_client.query(
        "INSERT INTO saga (id, title, saga_episode_start, saga_episode_end) VALUES (?, ?, ?, ?)",
        (saga_data["id"], saga_data["title"], saga_episode_start, saga_episode_end)
    )

    # Verify the data was inserted correctly
    result = db_client.query("SELECT * FROM saga WHERE id = ?", (saga_data["id"],))
    print(result)
    assert len(result) == 1
    assert result[0] == (saga_data["id"], saga_data["title"], saga_episode_start, saga_episode_end)

def test_insert_episode(db_client):
    # Example episode data
    episode_data = {
        "id": 1,
        "title": "Episode 1",
        "description": "The beginning of the adventure",
        "saga_id": 2
    }

    # Insert the episode data into the episode table
    db_client.query(
        "INSERT INTO episode (id, title, description, saga_id) VALUES (?, ?, ?, ?)",
        (episode_data["id"], episode_data["title"], episode_data["description"], episode_data["saga_id"])
    )

    # Verify the data was inserted correctly
    result = db_client.query("SELECT * FROM episode WHERE id = ?", (episode_data["id"],))
    assert len(result) == 1
    assert result[0] == (episode_data["id"], episode_data["title"], episode_data["description"], episode_data["saga_id"])


def test_insert_watched_episode(db_client):
    # Example watched episode data
    watched_episode_data = {
        "episode_id": 1,
        "workout_id": 1,
        "watched_date": "2023-10-01"
    }

    # Insert the watched episode data into the watched_episode table
    db_client.query(
        "INSERT INTO watched_episode (episode_id, workout_id, watched_date) VALUES (?, ?, ?)",
        (watched_episode_data["episode_id"], watched_episode_data['workout_id'],watched_episode_data["watched_date"])
    )

    # Verify the data was inserted correctly
    result = db_client.query("SELECT * FROM watched_episode WHERE episode_id = ? AND workout_id = ?", (watched_episode_data["episode_id"],watched_episode_data['workout_id']))
    print(result, watched_episode_data)
    assert len(result) == 1
    assert result[0] == (watched_episode_data["episode_id"], watched_episode_data["workout_id"], watched_episode_data["watched_date"])

def test_insert_workout(db_client):
    # Example workout data
    workout_data = {
        "id": 1,
        "date": "2023-10-01",
        "distance": 30,
        "work": 300
    }

    # Insert the workout data into the workout table
    db_client.query(
        "INSERT INTO workout (id, distance, work, date) VALUES (?, ?, ?, ?)",
        (workout_data["id"], workout_data["distance"], workout_data["work"],  workout_data["date"])
    )

    # Verify the data was inserted correctly
    result = db_client.query("SELECT * FROM workout WHERE id = ?", (workout_data["id"],))
    assert len(result) == 1
    assert result[0] == (workout_data["id"],  workout_data["distance"], workout_data["work"], workout_data["date"])

def parse_saga_episode(saga_episode):
    # Split the saga_episode string on the delimiter "à"
    parts = saga_episode.split("à")
    if len(parts) == 2:
        # Convert the parts to integers and return as a tuple
        return int(parts[0].strip()), int(parts[1].strip())
    else:
        raise ValueError("Invalid saga_episode format")