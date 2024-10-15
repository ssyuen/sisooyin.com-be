class Saga:
    def __init__(self, client=None):
        self.client = client
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS saga (id INTEGER PRIMARY KEY, title TEXT, saga_episode_start INTEGER, saga_episode_end INTEGER)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS saga (id INTEGER PRIMARY KEY, title TEXT, saga_episode_start INTEGER, saga_episode_end INTEGER)'
        self.client.query(query)
    def insert_saga(self, saga_data):
        query = 'INSERT INTO saga (id, title, saga_episode_start, saga_episode_end) VALUES (?, ?, ?, ?)'
        self.client.query(query, (saga_data["id"], saga_data["title"], saga_data["saga_episode_start"], saga_data["saga_episode_end"]))
        return self.client.cursor.lastrowid
    def insert_many_sagas(self, sagas_data):
        query = 'INSERT INTO saga (id, title, saga_episode_start, saga_episode_end) VALUES (?, ?, ?, ?)'        
        self.client.cursor.executemany(query, sagas_data)
        return self.client.cursor.lastrowid
    def get_sagas(self):
        query = 'SELECT * FROM saga'
        return self.client.query(query)
    def get_saga(self, saga_id):
        query = 'SELECT * FROM saga WHERE id = ?'
        return self.client.query(query, (saga_id,))
    def get_many_sagas(self, saga_ids):
        placeholders = ', '.join('?' for _ in saga_ids)
        query = f'SELECT * FROM saga WHERE id IN ({placeholders})'
        return self.client.query(query, saga_ids)
    def delete_saga(self, saga_id):
        query = 'DELETE FROM saga WHERE id = ?'
        self.client.query(query, (saga_id,))
        return self.client.cursor.rowcount
    def delete_many_sagas(self, saga_ids):
        placeholders = ', '.join('?' for _ in saga_ids)
        query = f'DELETE FROM saga WHERE id IN ({placeholders})'
        self.client.query(query, saga_ids)
        return self.client.cursor.rowcount