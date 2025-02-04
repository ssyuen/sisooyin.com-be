from flask import Blueprint ,request, jsonify

from app import get_db_client
from modules.db import blog_model
import os
from json import loads

blog_route = Blueprint("blog_route", __name__)
column_cache = {}

@blog_route.route("/api/blog/post/<post_id>", methods=["GET"])
def get_post_by_id(post_id):
    # Example route to demonstrate accessing the db_client
    db_client = get_db_client()
    blog = blog_model.Blog(db_client)
    result = blog.get_blog(post_id)
    print(result)
    if blog.table_name not in column_cache:
        column_names = blog.client.get_column_names(blog.table_name)
        column_cache[blog.table_name] = column_names
    else:
        column_names = column_cache[blog.table_name]
    
    if result:
        payload = dict(zip(column_names, result[0]))
        return jsonify(payload)
    else:
        return jsonify({"error": "Post not found"}), 404
    
@blog_route.route('/api/blog/post/delete/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        result = blog.delete_blog(post_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blog_route.route('/api/blog/posts/bulk_delete/<post_ids>', methods=['DELETE'])
def delete_many_posts(post_ids):
    try:
        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        result = blog.delete_many_blogs(post_ids)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blog_route.route("/api/blog/post/add", methods=["POST"])
def add_post():
    print(request.get_json())
    try:
        data = request.get_json()
        print(data)
        if 'title' not in data or 'tags' not in data or 'content' not in data or 'isPasswordLocked' not in data or 'date' not in data:
            return jsonify({'error': 'Title, tags, and content, date are required'}), 400

        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        inserted_id = blog.insert_blog(data)
        return jsonify({'success': 'Post added successfully', 'id': inserted_id})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    
@blog_route.route("/api/blog/posts", methods=["GET"])
def get_posts():
    db_client = get_db_client()
    blog = blog_model.Blog(db_client)
    result = blog.get_blogs()
    
    if blog.table_name not in column_cache:
        column_names = blog.client.get_column_names(blog.table_name)
        column_cache[blog.table_name] = column_names
    else:
        column_names = column_cache[blog.table_name]
    
    payload = [dict(zip(column_names, row)) for row in result]
    return jsonify(payload)

@blog_route.route("/api/blog/posts/<post_ids>", methods=["GET"])
def get_many_posts(post_ids):
    db_client = get_db_client()
    blog = blog_model.Blog(db_client)
    result = blog.get_many_blogs(post_ids)
    return jsonify(result)

@blog_route.route("/api/blog/posts/bulk_add", methods=["POST"])
def bulk_add_posts():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        response = blog.insert_many_blogs(data)
        print(response)
        return jsonify({'success': 'Posts added successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blog_route.route("/api/blog/posts/update", methods=["PUT"])
def update_post():
    try:
        data = request.get_json()
        if 'id' not in data:
            return jsonify({'error': 'ID is required'}), 400

        if 'tags' in data and isinstance(data['tags'], list):
            data['tags'] = ','.join(data['tags'])
        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        blog.update_blog(data)
        return jsonify({'success': 'Post updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@blog_route.route("/api/blog/posts/update_many", methods=["PUT"])
def update_many_posts():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        db_client = get_db_client()
        blog = blog_model.Blog(db_client)
        blog.update_many_blogs(data)
        return jsonify({'success': 'Posts updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    