import pytest
import os
from client import Client
from utils import get_daily_db_file
from booklog_model import Booklog

@pytest.fixture(scope="module")
def booklog():
    """
    Fixture to set up and tear down a BookLog instance with a temporary test database.

    Yields:
        BookLog: An instance of the BookLog class connected to the temporary test database.
    """
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    booklog = Booklog(client)

    # Create temporary tables
    booklog.create_table(temporary=True)

    yield booklog

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_booklog(booklog):
    # Example booklog data
    booklog_data = {
        "id": 1,
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5.0
    }
    
    # Insert the booklog data into the booklog table
    booklog.insert_book(booklog_data)

    # Verify the data was inserted correctly
    result = booklog.get_book(booklog_data["id"])
    assert len(result) == 1
    assert result[0] == (booklog_data["id"], booklog_data["title"], booklog_data["author"], booklog_data["pages"], booklog_data["rating"])
    booklog.delete_book(booklog_data["id"])

def test_insert_many_booklogs(booklog):
    # Example booklog data
    booklog_data = [
        ("Book 1", "Author 1", 100, 5.0),
        ("Book 2", "Author 2", 100, 4.0),
        ("Book 3", "Author 3", 100, 3.0)
    ]
    
    # Insert the booklog data into the booklog table
    booklog.insert_many_books(booklog_data)

    # Verify the data was inserted correctly
    result = booklog.get_books()
    assert len(result) == 3
    for i in range(3):
        assert result[i][1:] == booklog_data[i]
    booklog.delete_many_books([booklog_data[i][0] for i in range(3)])

def test_get_many_booklogs(booklog):
    # Example booklog data
    booklog_data = [
        ("Book 1", "Author 1", 100, 5.0),
        ("Book 2", "Author 2", 100, 4.0),
        ("Book 3", "Author 3", 100, 3.0)
    ]
    
    # Insert the booklog data into the booklog table
    booklog.insert_many_books(booklog_data)

    # Verify the data was inserted correctly
    result = booklog.get_many_books([1, 2])
    assert len(result) == 2
    for i in range(2):
        assert result[i][1:] == booklog_data[i]
    booklog.delete_many_books([booklog_data[i][0] for i in range(3)])

def test_get_booklog(booklog):
    # Example booklog data
    booklog_data = {
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5
    }
    
    # Insert the booklog data into the booklog table
    inserted_id = booklog.insert_book(booklog_data)

    # Retrieve the booklog data
    result = booklog.get_book(inserted_id)

    # Verify the data was retrieved correctly
    assert len(result) == 1
    assert result[0] == (inserted_id, booklog_data["title"], booklog_data["author"], booklog_data["pages"], booklog_data["rating"])
    booklog.delete_book(inserted_id)

def test_delete_booklog(booklog):
    # Example booklog data
    booklog_data = {
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5
    }
    
    # Insert the booklog data into the booklog table
    inserted_id = booklog.insert_book(booklog_data)

    # Verify the data was inserted correctly
    result = booklog.get_book(inserted_id)
    
    
    assert len(result) == 1
    assert result[0] == (inserted_id, booklog_data["title"], booklog_data["author"], booklog_data["pages"], booklog_data["rating"])

    # Delete the booklog data
    booklog.delete_book(inserted_id)

    # Verify the data was deleted
    result = booklog.get_book(inserted_id)
    assert len(result) == 0
