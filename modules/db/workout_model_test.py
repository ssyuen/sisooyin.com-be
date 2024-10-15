import pytest
import os
from client import Client
from utils import get_daily_db_file
from workout_model import Workout

@pytest.fixture(scope="module")
def workout():
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    workout = Workout(client)

    # Create temporary tables
    workout.create_table(temporary=True)

    yield workout

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_workout(workout):
    # Example workout data
    workout_data = {
        "id": 1,
        "distance": 5,
        "work": 2.5,
        "date": "2021-01-01"
    }

    # Insert the workout data into the workout table
    workout.insert_workout(workout_data)

    # Verify the data was inserted correctly
    result = workout.get_workout(workout_data["id"])
    assert len(result) == 1
    assert result[0] == (workout_data["id"], workout_data["distance"], workout_data["work"], workout_data["date"])
    workout.delete_workout(workout_data["id"])

def test_insert_many_workouts(workout):
    # Example workout data
    workout_data = [
        (1, 5, 2.5, "2021-01-01"),
        (2, 10, 5.0, "2021-01-02"),
        (3, 15, 7.5, "2021-01-03")
    ]

    # Insert the workout data into the workout table
    workout.insert_many_workouts(workout_data)

    # Verify the data was inserted correctly
    result = workout.get_workouts()
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (workout_data[i][0], workout_data[i][1], workout_data[i][2], workout_data[i][3])
    workout.delete_many_workouts([workout_data[i][0] for i in range(3)])

def test_get_many_workouts(workout):
    # Example workout data
    workout_data = [
        (1, 5, 2.5, "2021-01-01"),
        (2, 10, 5.0, "2021-01-02"),
        (3, 15, 7.5, "2021-01-03")
    ]

    # Insert the workout data into the workout table
    workout.insert_many_workouts(workout_data)

    # Verify the data was inserted correctly
    result = workout.get_workouts()
    assert len(result) == 3
    for i in range(3):
        assert result[i] == (workout_data[i][0], workout_data[i][1], workout_data[i][2], workout_data[i][3])
    workout.delete_many_workouts([workout_data[i][0] for i in range(3)])

def test_get_workouts_by_date(workout):
    # Example workout data
    workout_data = [
        (1, 5, 2.5, "2021-01-01"),
        (2, 10, 5.0, "2021-01-02"),
        (3, 15, 7.5, "2021-01-03")
    ]

    # Insert the workout data into the workout table
    workout.insert_many_workouts(workout_data)

    # Retrieve the workout data
    result = workout.get_workouts_by_date("2021-01-02")

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (2, 10, 5.0, "2021-01-02")
    workout.delete_many_workouts([workout_data[i][0] for i in range(3)])

def test_get_workout(workout):
    # Example workout data
    workout_data = {
        "id": 1,
        "distance": 5,
        "work": 2.5,
        "date": "2021-01-01"
    }

    # Insert the workout data into the workout table
    workout.insert_workout(workout_data)

    # Retrieve the workout data
    result = workout.get_workout(workout_data["id"])

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (workout_data["id"], workout_data["distance"], workout_data["work"], workout_data["date"])
    workout.delete_workout(workout_data["id"])

def test_delete_workout(workout):
    # Example workout data
    workout_data = {
        "id": 1,
        "distance": 5,
        "work": 2.5,
        "date": "2021-01-01"
    }

    # Insert the workout data into the workout table
    workout.insert_workout(workout_data)

    # Delete the workout data from the workout table
    workout.delete_workout(workout_data["id"])

    # Verify the data was deleted correctly
    result = workout.get_workout(workout_data["id"])
    assert len(result) == 0

def test_delete_many_workouts(workout):
    # Example workout data
    workout_data = [
        (1, 5, 2.5, "2021-01-01"),
        (2, 10, 5.0, "2021-01-02"),
        (3, 15, 7.5, "2021-01-03")
    ]

    # Insert the workout data into the workout table
    workout.insert_many_workouts(workout_data)

    # Delete the workout data from the workout table
    workout.delete_many_workouts([workout_data[i][0] for i in range(3)])

    # Verify the data was deleted correctly
    result = workout.get_workouts()
    assert len(result) == 0