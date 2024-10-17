from flask import Blueprint ,request, jsonify

from app import get_db_client
from modules.db import episode_model
import os
from json import loads

episode_route = Blueprint("episode_route", __name__)

@episode_route.route("/api/one_piece/saga/<saga_id>", methods=["GET"])
def get_episodes_by_saga(saga_id):
    saga_cache = {}
    try:
        # Check if the saga data is already in the cache
        if saga_id in saga_cache:
            return jsonify(saga_cache[saga_id])

        file_path = f"data/sagas/{saga_id}.json"
        if not os.path.exists(file_path):
            return jsonify({"error": "Saga not found"}), 404

        with open(file_path, "r") as file:
            saga_data = loads(file.read())
        
        # Store the saga data in the cache
        saga_cache[saga_id] = saga_data
        return jsonify(saga_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@episode_route.route("/api/one_piece/episode/<episode_id>", methods=["GET"])
def get_episode_by_id(episode_id):
    # Example route to demonstrate accessing the db_client
    db_client = get_db_client()
    episode = episode_model.Episode(db_client)
    result = episode.get_episode(episode_id)
    if result:
        return jsonify(result[0])
    else:
        return jsonify({"error": "Episode not found"}), 404
   
@episode_route.route('/api/one_piece/episode/delete/<episode_id>', methods=['DELETE'])
def delete_episode(episode_id):
    try:
        db_client = get_db_client()
        episode = episode_model.Episode(db_client)
        result = episode.delete_episode(episode_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@episode_route.route("/api/one_piece/episode/add", methods=["POST"])
def add_episode():
    try:
        data = request.get_json()
        if 'title' not in data or 'description' not in data or 'saga_id' not in data:
            return jsonify({'error': 'Title, description, and saga_id are required'}), 400

        db_client = get_db_client()
        episode = episode_model.Episode(db_client)
        result = episode.insert_episode(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500