class WatchedEpisode:
    def __init__(self, client=None):
        self.client = client
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS watched_episode (episode_id INTEGER, workout_id INTEGER, watched_date TEXT)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS watched_episode (episode_id INTEGER, workout_id INTEGER, watched_date TEXT)'
        self.client.query(query)
    def insert_watched_episode(self, watched_episode_data):
        query = 'INSERT INTO watched_episode (episode_id, workout_id, watched_date) VALUES (?, ?, ?)'
        self.client.query(query, (watched_episode_data["episode_id"], watched_episode_data["workout_id"], watched_episode_data["watched_date"]))
        return self.client.cursor.lastrowid
    def insert_many_watched_episodes(self, watched_episodes_data):
        query = 'INSERT INTO watched_episode (episode_id, workout_id, watched_date) VALUES (?, ?, ?)'
        self.client.cursor.executemany(query, watched_episodes_data)
        return self.client.cursor
    def get_watched_episodes_by_workout_id(self, workout_id):
        query = 'SELECT * FROM watched_episode WHERE workout_id = ?'
        return self.client.query(query, (workout_id,))
    def get_watched_episodes(self):
        query = 'SELECT * FROM watched_episode'
        return self.client.query(query)
    def get_watched_episode(self, episode_id, workout_id):
        query = 'SELECT * FROM watched_episode WHERE episode_id = ? AND workout_id = ?'
        return self.client.query(query, (episode_id, workout_id))
    def get_many_watched_episodes(self, watched_episode_ids):
        placeholders = ', '.join('?' for _ in watched_episode_ids)
        query = f'SELECT * FROM watched_episode WHERE episode_id IN ({placeholders})'
        return self.client.query(query, watched_episode_ids)
    def delete_watched_episode(self, episode_id, workout_id):
        query = 'DELETE FROM watched_episode WHERE episode_id = ? AND workout_id = ?'
        self.client.query(query, (episode_id, workout_id))
        return self.client.cursor.rowcount
    def delete_many_watched_episodes(self, watched_episode_ids):
        placeholders = ', '.join('?' for _ in watched_episode_ids)
        query = f'DELETE FROM watched_episode WHERE episode_id IN ({placeholders})'
        self.client.query(query, watched_episode_ids)
        return self.client.cursor.rowcount
    