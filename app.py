from flask import Flask, jsonify, request
from modules.peloton_wrapper import PelotonClient
import os
from flask_cors import CORS
from json import loads, dumps


app = Flask(__name__)
CORS(app)


@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    client = PelotonClient(username=os.environ["P_EMAIL"], password=os.environ["P_PW"])
    workouts = client.fetch_workouts()
    weekly_workouts = client.accumulate_work_and_distance(workouts)
    return jsonify(weekly_workouts)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
