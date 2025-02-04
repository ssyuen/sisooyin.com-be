import pytest
import os
from client import Client
from utils import get_daily_db_file
from blog_model import Blog

@pytest.fixture(scope="module")
def blog():
    """
    Fixture to set up and tear down a Blog instance with a temporary test database.

    Yields:
        Blog: An instance of the Blog class connected to the temporary test database.
    """
    # Setup: Create a Client instance with a test database file
    db_file = get_daily_db_file(testing=True)
    client = Client(db_file)
    blog = Blog(client)

    # Create temporary tables
    blog.create_table(temporary=True)

    yield blog

    # Teardown: Close the client connection and remove the test database file
    client.__del__()
    if os.path.exists(db_file):
        os.remove(db_file)

def test_insert_blog(blog):
    # Example blog data
    blog_data = {
        "id": 1,
        "title": "Blog 1",
        "tags": "tag1, tag2, tag3",
        "date": "2021-01-01",
        "content": "Content 1",
        "isPasswordLocked": 0
    }
    
    # Insert the blog data into the blog table
    blog.insert_blog(blog_data)

    # Verify the data was inserted correctly
    result = blog.get_blog(blog_data["id"])
    assert len(result) == 1
    assert result[0] == (blog_data["id"], blog_data["title"], blog_data["content"], blog_data["tags"] ,blog_data["date"], 0)
    blog.delete_blog(blog_data["id"])

def test_insert_many_blogs(blog):
    # Example blog data
    blog_data = [
            {
                "title": "Post 1",
                "content": "Content 1",
                "tags": "tag1, tag2",
                "date": "2021-01-01",
                "isPasswordLocked": 0
            },
            {
                "title": "Post 2",
                "content": "Content 2",
                "tags": "tag3, tag4",
                "date": "2021-01-02",
                "isPasswordLocked": 0
            }
        ]
    
    # Insert the blog data into the blog table
    blog.insert_many_blogs(blog_data)
    result = blog.get_blogs()
    assert len(result) == 2

    # Verify the data was inserted correctly
    for i, data in enumerate(blog_data):
        assert result[i] == (i+1, data["title"], data["content"], data["tags"], data["date"], 0)
    blog.delete_many_blogs([1, 2])

def test_get_blog(blog):
    # Example blog data
    blog_data = {
        "id": 1,
        "title": "Blog 1",
        "tags": "tag1, tag2, tag3",
        "date": "2021-01-01",
        "content": "Content 1",
        "isPasswordLocked": 0
    }
    
    # Insert the blog data into the blog table
    blog.insert_blog(blog_data)

    # Retrieve the blog by its ID
    result = blog.get_blog(blog_data["id"])
    assert len(result) == 1
    assert result[0] == (blog_data["id"], blog_data["title"], blog_data["content"], blog_data["tags"] ,blog_data["date"], 0)
    blog.delete_blog(blog_data["id"])

def test_get_many_blogs(blog):
    # Example blog data
    blog_data = [
        ("Blog 1", "Tag 1, Tag 2", "Content 1", "2021-01-01", 0),
        ("Blog 2", "Tag 1, Tag 2", "Content 2", "2021-01-02", 0),
        ("Blog 3", "Tag 1, Tag 2", "Content 3", "2021-01-03", 0)
    ]
    
    # Insert the blog data into the blog table
    blog.insert_many_blogs(blog_data)

    # Retrieve multiple blogs by their IDs
    result = blog.get_many_blogs([1, 2])
    assert len(result) == 2
    for i, data in enumerate(blog_data[:2]):
        assert result[i] == (i+1, data[0], data[1], data[2], data[3])
    blog.delete_many_blogs([1, 2, 3])

def test_delete_blog(blog):
    # Example blog data
    blog_data = {
        "id": 1,
        "title": "Blog 1",
        "tags": "tag1, tag2, tag3",
        "date": "2021-01-01",
        "content": "Content 1"
    }
    
    # Insert the blog data into the blog table
    blog.insert_blog(blog_data)

    # Delete the blog by its ID
    result = blog.delete_blog(blog_data["id"])
    assert result == 1

def test_delete_many_blogs(blog):
    # Example blog data
    blog_data = [
        ("Blog 1", "Tag 1, Tag 2", "Content 1", "2021-01-01"),
        ("Blog 2", "Tag 1, Tag 2", "Content 2", "2021-01-02"),
        ("Blog 3", "Tag 1, Tag 2", "Content 3", "2021-01-03")
    ]
    
    # Insert the blog data into the blog table
    blog.insert_many_blogs(blog_data)

    # Delete multiple blogs by their IDs
    result = blog.delete_many_blogs([1, 2])
    assert result == 2
    result = blog.get_blogs()
    assert len(result) == 1
    blog.delete_many_blogs([1, 2, 3])

def test_update_blog(blog):
    # Example blog data
    blog_data = {
        "id": 1,
        "title": "Blog 1",
        "tags": "tag1, tag2, tag3",
        "date": "2021-01-01",
        "content": "Content 1"
    }
    
    # Insert the blog data into the blog table
    blog.insert_blog(blog_data)

    # Update the blog data
    updated_data = {
        "id": 1,
        "title": "Blog 1 Updated",
        "tags": "tag 1, tag 2, tag 4",
        "content": "Content 1 Updated"
    }
    blog.update_blog(updated_data)

    # Retrieve the updated blog data
    result = blog.get_blog(updated_data["id"])
    assert len(result) == 1
    assert result[0] == (updated_data["id"], updated_data["title"], updated_data["content"], updated_data["tags"], blog_data["date"])
    blog.delete_blog(updated_data["id"])

def test_update_many_blog(blog):
    # Example blog data
    blog_data = [
        ("Blog 1", "Tag 1, Tag 2", "Content 1", "2021-01-01"),
        ("Blog 2", "Tag 1, Tag 2", "Content 2", "2021-01-02"),
        ("Blog 3", "Tag 1, Tag 2", "Content 3", "2021-01-03")
    ]
    
    # Insert the blog data into the blog table
    blog.insert_many_blogs(blog_data)

    # Update multiple blogs
    updated_data = [
        {
            "id": 1,
            "title": "Title 1 Updated",        
            "content": "Content 1 Updated"
        },
        {
            "id": 2,
            "title": "Title 2 Updated",
            "content": "content 2 updated"
        }
    ]
    blog.update_many_blogs(updated_data)

    # Verify the data was updated correctly
    result = blog.get_many_blogs([1, 2])
    assert len(result) == 2
    for i, data in enumerate(updated_data):
        assert result[i] == (data["id"], data["title"],  data["content"], blog_data[i][2], blog_data[i][3])
    blog.delete_many_blogs([1, 2, 3])

