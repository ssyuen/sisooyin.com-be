from flask import Blueprint ,request, jsonify
import os


from modules.peloton_wrapper import PelotonClient

workouts_route = Blueprint("workouts_route", __name__)

@workouts_route.route("/api/workouts", methods=["GET"])
def get_workouts():
    client = PelotonClient(username=os.environ["P_EMAIL"], password=os.environ["P_PW"])
    workouts = client.fetch_workouts()
    weekly_workouts = client.accumulate_work_and_distance(workouts)
    return jsonify(weekly_workouts)