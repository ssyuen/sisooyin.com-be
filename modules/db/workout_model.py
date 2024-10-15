class Workout:
    def __init__(self, client=None):
        self.client = client
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS workout (id INTEGER PRIMARY KEY, distance FLOAT, work FLOAT, date TEXT)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS workout (id INTEGER PRIMARY KEY, distance FLOAT, work FLOAT, date TEXT)'
        self.client.query(query)

    def insert_workout(self, workout_data):
        query = 'INSERT INTO workout (id, distance, work, date) VALUES (?, ?, ?, ?)'
        self.client.query(query, (workout_data["id"], workout_data["distance"], workout_data["work"], workout_data["date"]))
        return self.client.cursor.lastrowid
    def insert_many_workouts(self, workouts_data):
        query = 'INSERT INTO workout (id, distance, work, date) VALUES (?, ?, ?, ?)'
        self.client.cursor.executemany(query, workouts_data)
        return self.client.cursor.lastrowid
    def get_workouts(self):
        query = 'SELECT * FROM workout'
        return self.client.query(query)
    def get_workouts_by_date(self, date):
        query = 'SELECT * FROM workout WHERE date = ?'
        return self.client.query(query, (date,))
    def get_many_workouts(self, workout_ids):
        placeholders = ', '.join('?' for _ in workout_ids)
        query = f'SELECT * FROM workout WHERE id IN ({placeholders})'
        return self.client.query(query, workout_ids)
    def get_workout(self, workout_id):
        query = 'SELECT * FROM workout WHERE id = ?'
        return self.client.query(query, (workout_id,))
    def delete_workout(self, workout_id):
        query = 'DELETE FROM workout WHERE id = ?'
        self.client.query(query, (workout_id,))
        return self.client.cursor.rowcount
    def delete_many_workouts(self, workout_ids):
        placeholders = ', '.join('?' for _ in workout_ids)
        query = f'DELETE FROM workout WHERE id IN ({placeholders})'
        self.client.query(query, workout_ids)
        return self.client.cursor.rowcount
    