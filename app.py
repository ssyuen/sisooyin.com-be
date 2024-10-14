from flask import Flask, jsonify, request
from modules.peloton_wrapper import PelotonClient
import os
from json import loads, dumps


app = Flask(__name__)


# Define a route for the API endpoint
@app.route("/api/data", methods=["GET"])
def get_data():
    # Example data to return
    data = {"message": "Hello, API!", "status": "success"}
    return jsonify(data)


@app.route("/api/workouts", methods=["GET"])
def get_workouts():
    client = PelotonClient(username=os.environ["P_EMAIL"], password=os.environ["P_PW"])
    workouts = client.fetch_workouts()
    
    return jsonify(workouts)


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
