from flask import Blueprint ,request, jsonify
import os

from modules.oura_wrapper import OuraClient

oura_route = Blueprint("oura_route", __name__)

@oura_route.route("/api/sleep", methods=["GET"])
def get_sleep():
    client = OuraClient(access_token=os.environ["OURA_PAT"])
    sleep_data = client.fetch_sleep_data(start_date=request.args.get("start_date"), end_date=request.args.get("end_date"))
    return jsonify(sleep_data)

@oura_route.route("/api/oura_workouts", methods=["GET"])
def get_workouts():
    client = OuraClient(access_token=os.environ["OURA_PAT"])
    workout_data = client.fetch_workout_data(start_date=request.args.get("start_date"), end_date=request.args.get("end_date"))
    return jsonify(workout_data)

@oura_route.route("/api/activity", methods=["GET"])
def get_activity():
    client = OuraClient(access_token=os.environ["OURA_PAT"])
    activity_data = client.fetch_daily_activity_data(start_date=request.args.get("start_date"), end_date=request.args.get("end_date"))
    return jsonify(activity_data)