import pytest
import os
from client import Client
from utils import get_daily_db_file, parse_saga_episode
from episode_model import Episode

@pytest.fixture(scope="module")
def episode():
    """
    Fixture to set up and tear down an Episode instance with a temporary test database.

    Yields:
        Episode: An instance of the Episode class connected to the temporary test database.
    """
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    episode = Episode(client)

    # Create temporary tables
    episode.create_table(temporary=True)

    yield episode

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_episode(episode):
    # Example episode data
    episode_data = {
        "id": 1,
        "title": "Episode 1",
        "description": "The beginning of the adventure",
        "saga_id": 2
    }
    
    # Insert the episode data into the episode table
    episode.insert_episode(episode_data)

    # Verify the data was inserted correctly
    result = episode.get_episode(episode_data["id"])
    assert len(result) == 1
    assert result[0] == (episode_data["id"], episode_data["title"], episode_data["description"], episode_data["saga_id"])
    episode.delete_episode(episode_data["id"])

def test_insert_many_episodes(episode):
    # Example episode data
    episode_data = [
        (1, "Episode 1", "The beginning of the adventure", 2),
        (2, "Episode 2", "The continuation of the adventure", 2),
        (3, "Episode 3", "The climax of the adventure", 2)
    ]
    
    # Insert the episode data into the episode table
    episode.insert_many_episodes(episode_data)

    # Verify the data was inserted correctly
    result = episode.get_episodes()
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (episode_data[i][0], episode_data[i][1], episode_data[i][2], episode_data[i][3])
    episode.delete_many_episodes([episode_data[i][0] for i in range(3)])

def test_get_many_episodes(episode):
    # Example episode data
    episode_data = [
        (1, "Episode 1", "The beginning of the adventure", 2),
        (2, "Episode 2", "The continuation of the adventure", 2),
        (3, "Episode 3", "The climax of the adventure", 2)
    ]
    
    # Insert the episode data into the episode table
    episode.insert_many_episodes(episode_data)

    # Retrieve the episode data
    result = episode.get_many_episodes([episode_data[i][0] for i in range(3)])

    # Verify the data was retrieved correctly
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (episode_data[i][0], episode_data[i][1], episode_data[i][2], episode_data[i][3])
    episode.delete_many_episodes([episode_data[i][0] for i in range(3)])

def test_get_episode(episode):
    # Example episode data
    episode_data = {
        "id": 1,
        "title": "Episode 1",
        "description": "The beginning of the adventure",
        "saga_id": 2
    }
    
    # Insert the episode data into the episode table
    episode.insert_episode(episode_data)

    # Retrieve the episode data
    result = episode.get_episode(episode_data["id"])

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (episode_data["id"], episode_data["title"], episode_data["description"], episode_data["saga_id"])
    episode.delete_episode(episode_data["id"])

def test_delete_episode(episode):
    # Example episode data
    episode_data = {
        "id": 1,
        "title": "Episode 1",
        "description": "The beginning of the adventure",
        "saga_id": 2
    }
    
    # Insert the episode data into the episode table
    episode.insert_episode(episode_data)

    # Delete the episode data
    result = episode.delete_episode(episode_data["id"])

    # Verify the data was deleted correctly
    assert result == 1
    result = episode.get_episode(episode_data["id"])
    assert len(result) == 0


