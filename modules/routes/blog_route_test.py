import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Now you can import the app module
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_and_delete_blog_by_id(client):
    # Insert test post first
    post_data = {
        "title": "Post 1",
        "content": "Content 1",
        "tags": "tag1, tag2",
        "date": "2021-01-01"
    }
    response = client.post("/api/blog/post/add", json=post_data)
    inserted_id = response.json.get("id")
    print(inserted_id)
    assert response.status_code == 200

    response = client.get(f"/api/blog/post/{inserted_id}")
    assert response.status_code == 200

    response = client.delete("/api/blog/post/delete/1")
    assert response.status_code == 200

    response = client.get("/api/blog/post/1")
    assert response.status_code == 404

def test_add_blog(client):
    response = client.post(
        "/api/blog/post/add",
        json={
            "title": "Post 1",
            "content": "Content 1",
            "tags": "tag1, tag2",
            "date": "2021-01-01"
        }
    )
    inserted_id = response.json
    assert response.status_code == 200

    client.delete(f"/api/blog/post/delete/{inserted_id}")
    assert response.status_code == 200

def test_bulk_add_blogs(client):
    response = client.post(
        "/api/blog/posts/bulk_add",
        json=[
            {
                "title": "Post 1",
                "content": "Content 1",
                "tags": "tag1, tag2",
                "date": "2021-01-01"
            },
            {
                "title": "Post 2",
                "content": "Content 2",
                "tags": "tag3, tag4",
                "date": "2021-01-02"
            }
        ]
    )
    inserted_ids = response.json
    print(response.json)
    assert response.status_code == 200

    client.delete(f"/api/blog/posts/bulk_delete/{inserted_ids}")
    assert response.status_code == 200

def test_get_posts(client):
    response = client.get("/api/blog/posts")
    assert response.status_code == 200

def test_get_many_posts(client):
    response = client.get("/api/blog/posts/1,2")
    assert response.status_code == 200

def test_delete_many_posts(client):
    response = client.delete("/api/blog/posts/bulk_delete/1,2")
    assert response.status_code == 200

def test_delete_post(client):
    response = client.delete("/api/blog/post/delete/1")
    assert response.status_code == 200

def test_update_post(client):
    response = client.post(
        "/api/blog/post/add",
        json={
            "title": "Post 1",
            "content": "Content 1",
            "tags": "tag1, tag2",
            "date": "2021-01-01"
        }
    )
    inserted_id = response.json
    assert response.status_code == 200

    response = client.post(
        "/api/blog/post/update",
        json={
            "id": inserted_id,
            "title": "Post 2",
            "content": "Content 2",
            "tags": "tag3, tag4",
            "date": "2021-01-02"
        }
    )
    assert response.status_code == 200

    client.delete(f"/api/blog/post/delete/{inserted_id}")
    assert response.status_code == 200

def test_update_many_posts(client):
    response = client.post(
        "/api/blog/posts/bulk_add",
        json=[
            {
                "title": "Post 1",
                "content": "Content 1",
                "tags": "tag1, tag2",
                "date": "2021-01-01"
            },
            {
                "title": "Post 2",
                "content": "Content 2",
                "tags": "tag3, tag4",
                "date": "2021-01-02"
            }
        ]
    )
    inserted_ids = response.json
    assert response.status_code == 200

    response = client.post(
        "/api/blog/posts/update_many",
        json=[
            {
                "id": inserted_ids[0],
                "title": "Post 3",
                "content": "Content 3",
                "tags": "tag5, tag6",
                "date": "2021-01-03"
            },
            {
                "id": inserted_ids[1],
                "title": "Post 4",
                "content": "Content 4",
                "tags": "tag7, tag8",
                "date": "2021-01-04"
            }
        ]
    )
    assert response.status_code == 200

    client.delete(f"/api/blog/posts/bulk_delete/{inserted_ids}")
    assert response.status_code == 200