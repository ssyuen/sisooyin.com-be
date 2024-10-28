import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import json
load_dotenv()

# Global vars
USER_AGENT = "web"
API_BASE_URL = "https://api.ouraring.com"
API_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": USER_AGENT,
}

class OuraClient:
    """Primary client class for accessing Oura API methods in Python."""

    def __init__(self, access_token=None):
        if not access_token:
            raise ValueError("Oura access token not provided.")

        self.access_token = access_token
        self.session = self._init_session()

    def _init_session(self):
        """Initializes API client with provided access token"""
        api_session = requests.Session()
        api_session.headers.update({"Authorization": f"Bearer {self.access_token}"})

        return api_session

    def _call_api(self, request_uri, request_parameters):
        """Performs calls against Oura API endpoints."""
        response = self.session.get(
            API_BASE_URL + request_uri,
            headers=API_HEADERS,
            params=request_parameters,
        )

        if response.status_code != 200:
            raise ValueError("API request failed. Check endpoint and parameters.")

        return response.json()
    
    def fetch_workout_data(self, start_date, end_date):
        """Fetches workout data from Oura API."""
        request_uri = "/v2/usercollection/workout"

        # Ensure start_date and end_date are in YYYY-MM-DD format
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        request_parameters = {
            "start_date": start_date,
            "end_date": end_date,
        }

        response = self._call_api(request_uri, request_parameters)

        formatted_response = []
        for workout in response['data']:
            formatted_workout = {
                "date": workout["day"],
                "activity": workout["activity"],                                
            }
            formatted_response.append(formatted_workout)

        # Group formatted_response by activity
        grouped_response = {}
        for workout in formatted_response:
            activity = workout["activity"]
            if activity not in grouped_response:
                grouped_response[activity] = []
            grouped_response[activity].append(workout)

        return grouped_response
        
    
    def fetch_sleep_data(self, start_date, end_date):
        """Fetches sleep data from Oura API."""
        request_uri = "/v2/usercollection/daily_sleep"

        # Ensure start_date and end_date are in YYYY-MM-DD format
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        request_parameters = {
            "start_date": start_date,
            "end_date": end_date,
        }

        response = self._call_api(request_uri, request_parameters)

        formatted_response = []
        for sleep in response['data']:
            formatted_sleep = {
                "date": sleep["day"],
                "score": sleep["score"],
            }
            formatted_response.append(formatted_sleep)

        # Sort formatted_response by date
        formatted_response.sort(key=lambda x: x["date"])

        return formatted_response
    
    def fetch_daily_activity_data(self, start_date, end_date):
        """Fetches daily activity data from Oura API."""
        request_uri = "/v2/usercollection/daily_activity"

        # Ensure start_date and end_date are in YYYY-MM-DD format
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        request_parameters = {
            "start_date": start_date,
            "end_date": end_date,
        }

        response = self._call_api(request_uri, request_parameters)

        # Convert the response to a more readable format
        formatted_response = []

        for activity in response['data']:
            formatted_activity = {
                "date": activity["day"],
                "activity_score": activity["score"],
                "steps": activity["equivalent_walking_distance"],
                "active_calories": activity["active_calories"],
                "total_calories": activity["total_calories"],
            }
            formatted_response.append(formatted_activity)
        
        # Sort formatted_response by date
        formatted_response.sort(key=lambda x: x["date"])
        return formatted_response