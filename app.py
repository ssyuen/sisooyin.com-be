from flask import Flask, jsonify, request, g
from modules.db.utils import get_daily_db_file

from flask_cors import CORS
from modules.db.client import Client

from dotenv import load_dotenv
from modules.db import saga_model, episode_model, workout_model, watched_episode_model, booklog_model

load_dotenv()


def get_db_client():
    if 'db_client' not in g:
        if app.testing:
            db_file = get_daily_db_file(testing=True)
        else:
            db_file = get_daily_db_file()
        models = [saga_model.Saga, episode_model.Episode,
                   workout_model.Workout, watched_episode_model.WatchedEpisode,
                   booklog_model.Booklog]
        g.db_client = Client(db_file, models=models)
        g.db_client.instantiate_tables()
    return g.db_client

def get_app():
    return app

def list_of_blueprints():
    from modules.routes.episode_route import episode_route
    # from modules.routes.saga_route import saga_route
    from modules.routes.workouts_route import workouts_route
    from modules.routes.watched_episode_route import watched_episode_route
    from modules.routes.booklog_route import booklog_route
    from modules.routes.oura_route import oura_route

    return [episode_route, workouts_route, 
            watched_episode_route, booklog_route,
            oura_route]



def create_app():
    app=Flask(__name__)
    for route in list_of_blueprints():
        app.register_blueprint(route)

    CORS(app)

    @app.teardown_appcontext
    def close_db_client(exception):
        # Add your teardown logic here
        pass

    @app.route("/")
    def home():
        return "Root"

    return app

app = create_app()

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
