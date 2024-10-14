import sqlite3
import os
import datetime
import glob

class Client:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor.fetchall()
    def dump_db(self, dump_type='db'):
        dump_dir = '/data/db/dumps'
        if not os.path.exists(dump_dir):
            os.makedirs(dump_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if dump_type == 'db':
            dump_file = os.path.join(dump_dir, f'dump_{timestamp}.db')
            backup_conn = sqlite3.connect(dump_file)
            with backup_conn:
                self.conn.backup(backup_conn)
            backup_conn.close()
        elif dump_type == 'sql':
            dump_file = os.path.join(dump_dir, f'dump_{timestamp}.sql')
            with open(dump_file, 'w') as f:
                for line in self.conn.iterdump():
                    f.write(f'{line}\n')

    def restore_db(self):
        dump_dir = '/data/db/dumps'
        list_of_files = glob.glob(os.path.join(dump_dir, 'dump_*.db'))
        if not list_of_files:
            raise FileNotFoundError("No dump files found in the directory")

        latest_file = max(list_of_files, key=os.path.getctime)
        backup_conn = sqlite3.connect(latest_file)
        with backup_conn:
            backup_conn.backup(self.conn)
        backup_conn.close()

    def __del__(self):
        self.conn.close()