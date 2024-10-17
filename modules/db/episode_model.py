class Episode:
    def __init__(self, client=None):
        self.client = client
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS episode (id INTEGER PRIMARY KEY, title TEXT, description TEXT, saga_id INTEGER)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS episode (id INTEGER PRIMARY KEY, title TEXT, description TEXT, saga_id INTEGER)'
        self.client.query(query)
    def insert_episode(self, episode_data):
        query = 'INSERT INTO episode (id, title, description, saga_id) VALUES (?, ?, ?, ?)'
        self.client.query(query, (episode_data["id"], episode_data["title"], episode_data["description"], episode_data["saga_id"]))
        return self.client.cursor.lastrowid
    def insert_many_episodes(self, episodes_data):
        query = 'INSERT INTO episode (id, title, description, saga_id) VALUES (?, ?, ?, ?)'
        print(query, episodes_data)
        self.client.cursor.executemany(query, episodes_data)
        return self.client.cursor.lastrowid
    def get_episodes(self):
        query = 'SELECT * FROM episode'
        return self.client.query(query)
    def get_episode(self, episode_id: int):
        """
        Get a single episode by its ID
        :param episode_id: int
        """
        query = 'SELECT * FROM episode WHERE id = ?'
        return self.client.query(query, (episode_id,))
    def get_many_episodes(self, episode_ids):
        placeholders = ', '.join('?' for _ in episode_ids)
        query = f'SELECT * FROM episode WHERE id IN ({placeholders})'
        return self.client.query(query, episode_ids)

    def delete_episode(self, episode_id):
        query = 'DELETE FROM episode WHERE id = ?'
        self.client.query(query, (episode_id,))
        return self.client.cursor.rowcount
    def delete_many_episodes(self, episode_ids):
        placeholders = ', '.join('?' for _ in episode_ids)
        query = f'DELETE FROM episode WHERE id IN ({placeholders})'
        self.client.query(query, episode_ids)
        return self.client.cursor.rowcount