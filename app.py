from flask import Flask, jsonify, request, g
from modules.db.utils import get_daily_db_file
from modules.peloton_wrapper import PelotonClient
import os
from flask_cors import CORS
from json import loads, dumps
from modules.db.client import Client


def get_db_client():
    if 'db_client' not in g:
        db_file = get_daily_db_file()
        g.db_client = Client(db_file)
    return g.db_client

app = Flask(__name__)
CORS(app)


# Cache dictionary to store saga data
saga_cache = {}

@app.teardown_appcontext
def close_db_client(exception):
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.__del__()

@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    client = PelotonClient(username=os.environ["P_EMAIL"], password=os.environ["P_PW"])
    workouts = client.fetch_workouts()
    weekly_workouts = client.accumulate_work_and_distance(workouts)
    return jsonify(weekly_workouts)

@app.route("/api/one_piece/saga/<saga_id>", methods=["GET"])
def get_episodes_by_saga(saga_id):
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

@app.route("/api/one_piece/watched", methods=["POST"])
def add_watched_episode():
    try:
        data = request.get_json()
        if "episode_id" not in data:
            return jsonify({"error": "Episode ID are required"}), 400

        saga_id = data["saga_id"]
        episode_id = data["episode_id"]
        watched_date = data["watched_date"]
        workout_id = data["workout_id"]

        file_path = f"data/sagas/{saga_id}.json"
        if not os.path.exists(file_path):
            return jsonify({"error": "Saga not found"}), 404

        with open(file_path, "r") as file:
            saga_data = loads(file.read())
        
        for episode in saga_data["episodes"]:
            if episode["id"] == episode_id:
                episode["watched"] = True
                break
        
        with open(file_path, "w") as file:
            file.write(dumps(saga_data, indent=4))
        
        # Update the cache
        saga_cache[saga_id] = saga_data

        # Use the db_client to update the database if needed
        db_client = get_db_client()
        db_client.query(
            "INSERT INTO watched_episodes (episode_id, workout_id, watched_date) VALUES (?, ?, ?)",
            (episode_id, workout_id, dumps(watched_date))
        )
        return jsonify(saga_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/one_piece/episode/<episode_id>", methods=["GET"])
def get_episode_by_id(episode_id):
    # Example route to demonstrate accessing the db_client
    db_client = get_db_client()
    result = db_client.query("SELECT * FROM episodes WHERE id = ?", (episode_id,))
    if result:
        return jsonify(result[0])
    else:
        return jsonify({"error": "Episode not found"}), 404
    

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
