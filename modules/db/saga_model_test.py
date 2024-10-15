import pytest
import os
from client import Client
from utils import get_daily_db_file
from saga_model import Saga

@pytest.fixture(scope="module")
def saga():
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)    
    saga = Saga(client)

    # Create temporary tables
    saga.create_table(temporary=True)        

    yield saga

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_saga(saga):
    # Example saga data
    saga_data = {
        "id": 1,
        "title": "saga 1",
        "saga_episode_start": 1,
        "saga_episode_end": 2
    }
    
    # Insert the saga data into the saga table
    saga.insert_saga(saga_data)

    # Verify the data was inserted correctly
    result = saga.get_saga(saga_data["id"])
    assert len(result) == 1
    assert result[0] == (saga_data["id"], saga_data["title"], saga_data["saga_episode_start"], saga_data["saga_episode_end"])
    saga.delete_saga(saga_data["id"])

def test_insert_many_sagas(saga):
    # Example saga data
    saga_data = [
        (1, "Saga 1", 1, 2),
        (2, "Saga 2", 2, 3),
        (3, "Saga 3", 50, 70)
    ]
    
    # Insert the saga data into the saga table
    saga.insert_many_sagas(saga_data)

    # Verify the data was inserted correctly
    result = saga.get_sagas()
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (saga_data[i][0], saga_data[i][1], saga_data[i][2], saga_data[i][3])
    saga.delete_many_sagas([saga_data[i][0] for i in range(3)])

def test_get_many_sagas(saga):
    # Example saga data
    saga_data = [
        (1, "Saga 1", 1, 2),
        (2, "Saga 2", 3, 4),
        (3, "Saga 3", 50, 70)
    ]
    
    # Insert the saga data into the saga table
    saga.insert_many_sagas(saga_data)

    # Retrieve the saga data
    result = saga.get_many_sagas([saga_data[i][0] for i in range(3)])

    # Verify the data was retrieved correctly
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (saga_data[i][0], saga_data[i][1], saga_data[i][2], saga_data[i][3])
    saga.delete_many_sagas([saga_data[i][0] for i in range(3)])
    
def test_get_saga(saga):
    # Example saga data
    saga_data = {
        "id": 1,
        "title": "Saga 1",
        "saga_episode_start": 1,
        "saga_episode_end": 2
    }
    
    # Insert the saga data into the saga table
    saga.insert_saga(saga_data)

    # Retrieve the saga data
    result = saga.get_saga(saga_data["id"])

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (saga_data["id"], saga_data["title"], saga_data["saga_episode_start"], saga_data["saga_episode_end"])
    saga.delete_saga(saga_data["id"])

def test_delete_saga(saga):
    # Example saga data
    saga_data = {
        "id": 1,
        "title": "Saga 1",
        "saga_episode_start": 1,
        "saga_episode_end": 4
    }
    
    # Insert the saga data into the saga table
    saga.insert_saga(saga_data)

    # Delete the saga data
    result = saga.delete_saga(saga_data["id"])

    # Verify the data was deleted correctly
    assert result == 1
    result = saga.get_saga(saga_data["id"])
    assert len(result) == 0


