import sqlite3
import os
import datetime
import glob

class Client:
    """
    The Client class provides methods to interact with an SQLite database.

    This class allows for creating tables, executing queries, retrieving column names,
    dumping the database to a file, and restoring the database from a dump file. It also
    supports instantiating tables based on provided model classes.

    Attributes:
        conn (sqlite3.Connection): The SQLite database connection.
        cursor (sqlite3.Cursor): The cursor for executing SQL queries.
        models (list): A list of model classes to instantiate tables.

    Methods:
        __init__(db_path="", models=[]):
            Initializes the Client with a database path and a list of model classes.
        
        instantiate_tables():
            Instantiates tables for all provided model classes.
        
        query(query, params=()):
            Executes a single SQL query with optional parameters.
            Returns the fetched results.
        
        executemany(query, params):
            Executes a SQL query with multiple sets of parameters.
        
        get_column_names(table_name):
            Retrieves the column names for a given table.
            Returns a list of column names.
        
        dump_db(dump_type='db'):
            Dumps the database to a file. Supports 'db' and 'sql' dump types.
        
        restore_db():
            Restores the database from the most recent dump file.
    """
    def __init__(self, db_path="", models=[]):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.models = models

    def instantiate_tables(self):
        for model in self.models:
            t_model = model(self)
            t_model.create_table()
    def query(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        return self.cursor.fetchall()
    def executemany(self, query, params):
        self.cursor.executemany(query, params)
        self.conn.commit()
    def get_column_names(self, table_name):
        query = f"PRAGMA table_info({table_name})"
        result = self.query(query)
        return [row[1] for row in result]
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