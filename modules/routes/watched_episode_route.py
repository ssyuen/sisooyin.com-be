from flask import Blueprint ,request, jsonify
from app import get_db_client


from modules.db.watched_episode_model import WatchedEpisode

watched_episode_route = Blueprint("watched_episode_route", __name__)

@watched_episode_route.route("/api/one_piece/watched/add", methods=["POST"])
def add_watched_episode():
    try:
        data = request.get_json()
        if "episode_id" not in data:
            return jsonify({"error": "Episode ID are required"}), 400

        # Use the db_client to update the database if needed
        db_client = get_db_client()
        watched_episode = WatchedEpisode(db_client)
        result = watched_episode.insert_watched_episode(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@watched_episode_route.route("/api/one_piece/watched/<int:episode_id>&<int:workout_id>", methods=["GET"])
def get_watched_episode_by_episode_and_workout(episode_id, workout_id):
    try:         
        db_client = get_db_client()
        watched_episode = WatchedEpisode(db_client)
        result = watched_episode.get_watched_episode(episode_id=episode_id, workout_id=workout_id)
        if result:
            return jsonify(result[0])
        else:
            return jsonify({"error": "Watched episode not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@watched_episode_route.route("/api/one_piece/watched/<int:episode_id>&<int:workout_id>", methods=["DELETE"])
def delete_watched_episode(episode_id, workout_id):
    try:
        db_client = get_db_client()
        watched_episode = WatchedEpisode(db_client)
        result = watched_episode.delete_watched_episode(episode_id=episode_id, workout_id=workout_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


 
