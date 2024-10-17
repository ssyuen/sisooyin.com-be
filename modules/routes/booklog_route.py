from flask import Blueprint ,request, jsonify

from app import get_db_client
from modules.db import booklog_model
import os
from json import loads

booklog_route = Blueprint("booklog_route", __name__)
column_cache = {}

@booklog_route.route("/api/booklog/book/<book_id>", methods=["GET"])
def get_book_by_id(book_id):
    # Example route to demonstrate accessing the db_client
    db_client = get_db_client()
    booklog = booklog_model.Booklog(db_client)
    result = booklog.get_book(book_id)
    
    if booklog.table_name not in column_cache:
        column_names = booklog.client.get_column_names(booklog.table_name)
        column_cache[booklog.table_name] = column_names
    else:
        column_names = column_cache[booklog.table_name]
    
    if result:
        payload = dict(zip(column_names, result[0]))
        return jsonify(payload)
    else:
        return jsonify({"error": "Book not found"}), 404

@booklog_route.route('/api/booklog/book/delete/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        db_client = get_db_client()
        booklog = booklog_model.Booklog(db_client)
        result = booklog.delete_book(book_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booklog_route.route('/api/booklog/books/bulk_delete/<book_ids>', methods=['DELETE'])
def delete_many_books(book_ids):
    try:
        db_client = get_db_client()
        booklog = booklog_model.Booklog(db_client)
        result = booklog.delete_many_books(book_ids)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booklog_route.route("/api/booklog/book/add", methods=["POST"])
def add_book():
    try:
        data = request.get_json()
        if 'title' not in data or 'author' not in data or 'pages' not in data or 'rating' not in data:
            return jsonify({'error': 'Title, author, pages, and rating are required'}), 400

        db_client = get_db_client()
        booklog = booklog_model.Booklog(db_client)
        booklog_data = {
            "title": data["title"],
            "author": data["author"],
            "pages": data["pages"],
            "rating": data["rating"]
        }
        result = booklog.insert_book(booklog_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@booklog_route.route("/api/booklog/books", methods=["GET"])
def get_books():
    db_client = get_db_client()
    booklog = booklog_model.Booklog(db_client)
    result = booklog.get_books()


    if booklog.table_name not in column_cache:
        column_names = booklog.client.get_column_names(booklog.table_name)
        column_cache[booklog.table_name] = column_names
    else:
        column_names = column_cache[booklog.table_name]
    result = [dict(zip(column_names, row)) for row in result]
    
    return jsonify(result)

@booklog_route.route("/api/booklog/books/<book_ids>", methods=["GET"])
def get_books_by_ids(book_ids):
    db_client = get_db_client()
    booklog = booklog_model.Booklog(db_client)
    result = booklog.get_many_books(book_ids)
    return jsonify(result)

@booklog_route.route("/api/booklog/books/bulk_add", methods=["POST"])
def add_books():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        db_client = get_db_client()
        booklog = booklog_model.Booklog(db_client)
        booklog_data = [(book["title"], book["author"], book["pages"], book["rating"]) for book in data]
        booklog.insert_many_books(booklog_data)
        return jsonify(booklog_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@booklog_route.route("/api/booklog/book/update", methods=["PUT"])
def update_book():
    try:
        data = request.get_json()
        if 'id' not in data:
            return jsonify({'error': 'Book ID is required'}), 400

        db_client = get_db_client()
        booklog = booklog_model.Booklog(db_client)
        booklog_data = {
            "id": data["id"],
            "title": data["title"],
            "author": data["author"],
            "pages": data["pages"],
            "rating": data["rating"]
        }
        booklog.update_book(booklog_data)
        return jsonify(booklog_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500