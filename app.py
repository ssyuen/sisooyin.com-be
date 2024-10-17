from flask import Flask, jsonify, request, g
from modules.db.utils import get_daily_db_file

from flask_cors import CORS
from modules.db.client import Client

from dotenv import load_dotenv
from modules.db import saga_model, episode_model, workout_model, watched_episode_model

load_dotenv()


def get_db_client():
    if 'db_client' not in g:
        if app.testing:
            db_file = get_daily_db_file(testing=True)
        else:
            db_file = get_daily_db_file()
        models = [saga_model.Saga, episode_model.Episode, workout_model.Workout, watched_episode_model.WatchedEpisode]
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

    return [episode_route, workouts_route, watched_episode_route]

app = Flask(__name__)

for route in list_of_blueprints():
    app.register_blueprint(route)


CORS(app)

@app.teardown_appcontext
def close_db_client(exception):
    db_client = g.pop('db_client', None)
    if db_client is not None:
        db_client.__del__()


# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
