from flask import Blueprint, request, jsonify

from app import get_db_client
from modules.db import auth_model, user_model
import os
from json import loads

auth_route = Blueprint("auth_route", __name__)

@auth_route.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Username and password are required'}), 400

        db_client = get_db_client()
        auth = auth_model.Auth(db_client)
        result = auth.login(data["username"], data["password"])
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_route.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if 'username' not in data or 'password' not in data or 'email' not in data:
            return jsonify({'error': 'Username, password, and email are required'}), 400

        db_client = get_db_client()
        user = user_model.User(db_client)
        result = user.insert_user(data["username"], data["password"], data["email"])
        if result:
            return jsonify(result)
        else:
            return jsonify({"error": "User already exists"}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500