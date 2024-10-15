from client import Client
from utils import get_daily_db_file, parse_saga_episode

if __name__ == '__main__':
    db_file = get_daily_db_file()
    db_client = Client(db_file)
    db_client.query("CREATE TABLE IF NOT EXISTS episode (id INTEGER PRIMARY KEY, title TEXT, description TEXT, saga_id INTEGER)")
    db_client.query("CREATE TABLE IF NOT EXISTS watched_episode (episode_id INTEGER, workout_id INTEGER, watched_date TEXT)")
    db_client.query("CREATE TABLE IF NOT EXISTS saga (id INTEGER PRIMARY KEY, title TEXT, saga_episode_start TEXT, saga_episode_end TEXT)")
    db_client.query("CREATE TABLE IF NOT EXISTS workout (id INTEGER PRIMARY KEY, distance INTEGER, work FLOAT, date TEXT)")


    # Example saga data
    saga_data = {
        "id": 2,
        "title": "Alabasta",
        "saga_number": "2",
        "saga_chapitre": "101 à 216",
        "saga_volume": "12 à 23",
        "saga_episode": "62 \u00e0 143"
    }

    
    # Parse the saga_episode
    saga_episode_start, saga_episode_end = parse_saga_episode(saga_data["saga_episode"])

    # Insert the saga data into the saga table
    db_client.query(
        "INSERT INTO saga (id, title, saga_episode_start, saga_episode_end) VALUES (?, ?, ?, ?)",
        (saga_data["id"], saga_data["title"], saga_episode_start, saga_episode_end)
    )

    saga_data2 = {
        "id": 3,
        "title": "Skypiea",
        "saga_number": "3",
        "saga_chapitre": "218 à 302",
        "saga_volume": "24 à 32",
        "saga_episode": "144 à 195"
    }
    # Parse the saga_episode
    saga_episode_start, saga_episode_end = parse_saga_episode(saga_data2["saga_episode"])
    # Insert the saga data into the saga table
    db_client.query(
        "INSERT INTO saga (id, title, saga_episode_start, saga_episode_end) VALUES (?, ?, ?, ?)",
        (saga_data2["id"], saga_data2["title"], saga_episode_start, saga_episode_end)
    )
    # db_client.dump_db()
    # db_client.restore_db()
    db_client.conn.commit()
    db_client.__del__()

