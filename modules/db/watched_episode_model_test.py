import pytest
import os
from client import Client
from utils import get_daily_db_file
from watched_episode_model import WatchedEpisode

@pytest.fixture(scope="module")
def watched_episode():
    """
    Fixture to set up and tear down a WatchedEpisode instance with a temporary test database.

    This fixture creates a temporary database file and a Client instance connected to it.
    It then creates a WatchedEpisode instance and sets up the necessary temporary tables.
    After the tests are run, it closes the Client connection and removes the temporary database file.

    Yields:
        WatchedEpisode: An instance of the WatchedEpisode class connected to the temporary test database.
    """
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    watched_episode = WatchedEpisode(client)

    # Create temporary tables
    watched_episode.create_table(temporary=True)

    yield watched_episode

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_watched_episode(watched_episode):
    # Example watched episode data
    watched_episode_data = {
        "episode_id": 1,
        "workout_id": 1,
        "watched_date": "2021-01-01"
    }

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_watched_episode(watched_episode_data)

    # Verify the data was inserted correctly
    result = watched_episode.get_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])
    assert len(result) == 1
    assert result[0] == (watched_episode_data["episode_id"], watched_episode_data["workout_id"], watched_episode_data["watched_date"])
    watched_episode.delete_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])

def test_insert_many_watched_episodes(watched_episode):
    # Example watched episode data
    watched_episode_data = [
        (1, 1, "2021-01-01"),
        (2, 2, "2021-01-02"),
        (3, 3, "2021-01-03")
    ]

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_many_watched_episodes(watched_episode_data)

    # Verify the data was inserted correctly
    result = watched_episode.get_watched_episodes()
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (watched_episode_data[i][0], watched_episode_data[i][1], watched_episode_data[i][2])
    watched_episode.delete_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])

def test_get_many_watched_episodes(watched_episode):
    # Example watched episode data
    watched_episode_data = [
        (1, 1, "2021-01-01"),
        (2, 2, "2021-01-02"),
        (3, 3, "2021-01-03")
    ]

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_many_watched_episodes(watched_episode_data)

    # Verify the data was inserted correctly
    result = watched_episode.get_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (watched_episode_data[i][0], watched_episode_data[i][1], watched_episode_data[i][2])
    watched_episode.delete_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])

def test_get_watched_episodes(watched_episode):
    # Example watched episode data
    watched_episode_data = [
        (1, 1, "2021-01-01"),
        (2, 2, "2021-01-02"),
        (3, 3, "2021-01-03")
    ]

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_many_watched_episodes(watched_episode_data)

    # Retrieve the watched episode data
    result = watched_episode.get_watched_episodes()

    # Verify the data was retrieved correctly
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (watched_episode_data[i][0], watched_episode_data[i][1], watched_episode_data[i][2])
    watched_episode.delete_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])

def test_get_watched_episodes_by_workout_id(watched_episode):
    # Example watched episode data
    watched_episode_data = [
        (1, 1, "2021-01-01"),
        (2, 2, "2021-01-02"),
        (3, 3, "2021-01-03")
    ]

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_many_watched_episodes(watched_episode_data)

    # Retrieve the watched episode data
    result = watched_episode.get_watched_episodes_by_workout_id(1)

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (watched_episode_data[0][0], watched_episode_data[0][1], watched_episode_data[0][2])
    watched_episode.delete_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])

def test_get_watched_episode(watched_episode):
    # Example watched episode data
    watched_episode_data = {
        "episode_id": 1,
        "workout_id": 1,
        "watched_date": "2021-01-01"
    }

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_watched_episode(watched_episode_data)

    # Retrieve the watched episode data
    result = watched_episode.get_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (watched_episode_data["episode_id"], watched_episode_data["workout_id"], watched_episode_data["watched_date"])
    watched_episode.delete_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])

def test_delete_watched_episode(watched_episode):
    # Example watched episode data
    watched_episode_data = {
        "episode_id": 1,
        "workout_id": 1,
        "watched_date": "2021-01-01"
    }

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_watched_episode(watched_episode_data)

    # Delete the watched episode data
    result = watched_episode.delete_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])

    # Verify the data was deleted correctly
    assert result == 1
    result = watched_episode.get_watched_episode(watched_episode_data["episode_id"], watched_episode_data["workout_id"])
    assert len(result) == 0

def test_delete_many_watched_episodes(watched_episode):
    # Example watched episode data
    watched_episode_data = [
        (1, 1, "2021-01-01"),
        (2, 2, "2021-01-02"),
        (3, 3, "2021-01-03")
    ]

    # Insert the watched episode data into the watched episode table
    watched_episode.insert_many_watched_episodes(watched_episode_data)

    # Delete the watched episode data
    result = watched_episode.delete_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])

    # Verify the data was deleted correctly
    assert result == 3
    result = watched_episode.get_many_watched_episodes([watched_episode_data[i][0] for i in range(3)])
    assert len(result) == 0

