import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

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

        return self._call_api(request_uri, request_parameters)
    
    def fetch_sleep_data(self, start_date, end_date):
        """Fetches sleep data from Oura API."""
        request_uri = "/v2/usercollection/sleep"

        # Ensure start_date and end_date are in YYYY-MM-DD format
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        request_parameters = {
            "start": start_date,
            "end": end_date,
        }

        return self._call_api(request_uri, request_parameters)
    
    def fetch_daily_activity_data(self, start_date, end_date):
        """Fetches daily activity data from Oura API."""
        request_uri = "/v2/usercollection/daily_activity"

        # Ensure start_date and end_date are in YYYY-MM-DD format
        start_date = datetime.strptime(start_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d").strftime("%Y-%m-%d")
        request_parameters = {
            "start": start_date,
            "end": end_date,
        }

        return self._call_api(request_uri, request_parameters)