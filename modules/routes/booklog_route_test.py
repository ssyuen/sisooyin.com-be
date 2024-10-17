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

def test_get_and_delete_book_by_id(client):
    # Insert test book first
    book_data = {
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5
    }
    response = client.post("/api/booklog/book/add", json=book_data)
    inserted_id = response.json
    assert response.status_code == 200

    response = client.get(f"/api/booklog/book/{inserted_id}")
    assert response.status_code == 200

    response = client.delete("/api/booklog/book/delete/1")
    assert response.status_code == 200

    response = client.get("/api/booklog/book/1")
    assert response.status_code == 404

def test_add_book(client):    
    response = client.post(
        "/api/booklog/book/add",
        json={            
            "title": "Book 1",
            "author": "Author 1",
            "description": "Description 1",
            "pages": 100,
            "rating": 5
        }
    )
    inserted_id = response.json
    assert response.status_code == 200

    client.delete(f"/api/booklog/book/delete/{inserted_id}")
    assert response.status_code == 200

def test_bulk_add_books(client):
    response = client.post(
        "/api/booklog/books/bulk_add",
        json=[
            {
                "title": "Book 1",
                "author": "Author 1",
                "description": "Description 1",
                "pages": 100,
                "rating": 5
            },
            {
                "title": "Book 2",
                "author": "Author 2",
                "description": "Description 2",
                "pages": 200,
                "rating": 4
            }
        ]
    )
    print(response.json)
    assert response.status_code == 200

    client.delete("/api/booklog/book/bulk_delete/1&2")
    assert response.status_code == 200

def test_bulk_delete_books(client):
    # Insert test books first
    book_data = {
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5
    }
    response = client.post("/api/booklog/book/add", json=book_data)
    inserted_book_id_1 = response.json
    assert response.status_code == 200

    book_data["id"] = 2
    response = client.post("/api/booklog/book/add", json=book_data)
    inserted_book_id_2 = response.json
    assert response.status_code == 200

    response = client.delete(f"/api/booklog/books/bulk_delete/{inserted_book_id_1}&{inserted_book_id_2}")
    assert response.status_code == 200

def test_get_books(client):
    response = client.get("/api/booklog/books")
    assert response.status_code == 200

def test_get_books_by_ids(client):
    response = client.get("/api/booklog/books/1&2")
    assert response.status_code == 200

def test_update_book(client):
    # Insert test book first
    book_data = {
        "title": "Book 1",
        "author": "Author 1",
        "pages": 100,
        "rating": 5
    }
    response = client.post("/api/booklog/book/add", json=book_data)
    inserted_id = response.json
    assert response.status_code == 200

    update_payload = {
        "id": inserted_id,
        "title": "Book 2"
    }
    book_data.update(update_payload)
    response = client.put("/api/booklog/book/update", json=book_data)
    assert response.status_code == 200

    response = client.get(f"/api/booklog/book/{inserted_id}")
    print(response.json)
    assert response.status_code == 200
    assert response.json["title"] == "Book 2"

    response = client.delete(f"/api/booklog/book/delete/{inserted_id}")
    assert response.status_code == 200
