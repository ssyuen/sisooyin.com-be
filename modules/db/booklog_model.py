class Booklog:
    """
    The Booklog class provides methods to interact with the 'booklog' table in the database.
    
    This class allows for creating the table, inserting single or multiple book records, 
    retrieving single or multiple book records, updating book records, and deleting single 
    or multiple book records. It uses a Client instance to execute SQL queries.

    Attributes:
        client (Client): An instance of the Client class used to execute SQL queries.
        table_name (str): The name of the table this class interacts with, default is 'booklog'.

    Methods:
        create_table(temporary=False):
            Creates the 'booklog' table in the database. If temporary is True, creates a temporary table.
        
        insert_book(book_data):
            Inserts a single book record into the 'booklog' table.
            Returns the ID of the inserted record.
        
        insert_many_books(books_data):
            Inserts multiple book records into the 'booklog' table.
            Returns a list of IDs of the inserted records.
        
        get_books():
            Retrieves all book records from the 'booklog' table.
            Returns a list of tuples, each representing a book record.
        
        get_book(id):
            Retrieves a single book record by its ID.
            Returns a tuple representing the book record.
        
        get_many_books(ids):
            Retrieves multiple book records by their IDs.
            Returns a list of tuples, each representing a book record.
        
        delete_book(id):
            Deletes a single book record by its ID.
            Returns the number of rows affected.
        
        delete_many_books(ids):
            Deletes multiple book records by their IDs.
            Returns the number of rows affected.
        
        update_book(book_data):
            Updates a book record in the 'booklog' table.
            Returns the number of rows affected.
    """
    def __init__(self, client):
        self.client = client
        self.table_name = 'booklog'
    
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS booklog (id INTEGER PRIMARY KEY, title TEXT, author TEXT, pages INTEGER, rating FLOAT)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS booklog (id INTEGER PRIMARY KEY, title TEXT, author TEXT, pages INTEGER, rating FLOAT)'
        self.client.query(query)
    def insert_book(self, book_data):
        query = 'INSERT INTO booklog (title, author, pages, rating) VALUES ( ?, ?, ?, ?)'
        self.client.query(query, ( book_data["title"], book_data["author"], book_data["pages"], book_data["rating"]))
        return self.client.cursor.lastrowid
    def insert_many_books(self, books_data):
        query = 'INSERT INTO booklog (title, author, pages, rating) VALUES ( ?, ?, ?, ?)'
        self.client.cursor.executemany(query, books_data)
        last_ids = self.client.cursor.fetchall()
        print(last_ids)
        return last_ids
    def get_books(self):
        query = 'SELECT * FROM booklog'
        return self.client.query(query)
    def get_book(self, id: int):
        """
        Get a single book by its ID
        :param id: int
        """
        query = 'SELECT * FROM booklog WHERE id = ?'
        
        return self.client.query(query, (id,))
    def get_many_books(self, ids):
        placeholders = ', '.join('?' for _ in ids)
        query = f'SELECT * FROM booklog WHERE id IN ({placeholders})'
        return self.client.query(query, ids)
    def delete_book(self, id):
        query = 'DELETE FROM booklog WHERE id = ?'
        self.client.query(query, (id,))
        return self.client.cursor.rowcount
    def delete_many_books(self, ids):
        placeholders = ', '.join('?' for _ in ids)
        query = f'DELETE FROM booklog WHERE id IN ({placeholders})'
        self.client.query(query, ids)
        return self.client.cursor.rowcount
    def update_book(self, book_data):
        query = 'UPDATE booklog SET title = ?, author = ?, pages = ?, rating = ? WHERE id = ?'
        self.client.query(query, (book_data["title"], book_data["author"], book_data["pages"], book_data["rating"], book_data["id"]))
        return self.client.cursor.rowcount