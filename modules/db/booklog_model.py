class Booklog:
    def __init__(self, client):
        self.client = client
    
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS booklog (id INTEGER PRIMARY KEY, title TEXT, author TEXT, pages INTEGER, rating FLOAT)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS booklog (id INTEGER PRIMARY KEY, title TEXT, author TEXT, pages INTEGER, rating FLOAT)'
        self.client.query(query)
    def insert_book(self, book_data):
        query = 'INSERT INTO booklog (id, title, author, pages, rating) VALUES (?, ?, ?, ?, ?)'
        self.client.query(query, (book_data["id"], book_data["title"], book_data["author"], book_data["pages"], book_data["rating"]))
        return self.client.cursor.lastrowid
    def insert_many_books(self, books_data):
        query = 'INSERT INTO booklog (id, title, author, pages, rating) VALUES (?, ?, ?, ?, ?)'
        self.client.cursor.executemany(query, books_data)
        return self.client.cursor.lastrowid
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