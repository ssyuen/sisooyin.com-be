class Blog:
    def __init__(self, client):
        self.client = client
        self.table_name = 'blog'

    
    def create_table(self, temporary=False):
        if temporary:
            query = 'CREATE TEMPORARY TABLE IF NOT EXISTS blog (id INTEGER PRIMARY KEY, title TEXT, content TEXT, tags TEXT, date TEXT)'
        else:
            query = 'CREATE TABLE IF NOT EXISTS blog (id INTEGER PRIMARY KEY, title TEXT, content TEXT, tags TEXT, date TEXT)'
        self.client.query(query)

    def insert_blog(self, blog_data):
        """
        Inserts a single blog record into the 'blog' table.

        Returns the ID of the inserted record.

        :param blog_data: dict

        Example:
        blog_data = {
            "title": "Blog 1",
            "content": "Content 1",
            "tags": "tag1, tag2, tag3",
            "date": "2021-01-01"
        }
        """
        # if the tag data comes as an array, unpack it into a string separated by commas
        if isinstance(blog_data["tags"], list):
            blog_data["tags"] = ', '.join(blog_data["tags"])
        query = 'INSERT INTO blog (title, content, tags, date) VALUES ( ?, ?, ?, ?)'
        self.client.query(query, ( blog_data["title"], blog_data["content"], blog_data["tags"], blog_data["date"]))
        return self.client.cursor.lastrowid
    
    def insert_many_blogs(self, blogs_data):
        query = 'INSERT INTO blog (title, content, tags, date) VALUES ( ?, ?, ?, ?)'
        data_tuples = [(blog["title"], blog["content"], blog["tags"], blog["date"]) for blog in blogs_data]
        self.client.cursor.executemany(query, data_tuples)
        last_ids = self.client.cursor.lastrowid
        print(last_ids)
        return last_ids
    
    def get_blogs(self):
        query = 'SELECT * FROM blog'
        return self.client.query(query)
    
    def get_blog(self, id: int):
        """
        Get a single blog by its ID
        :param id: int
        """
        query = 'SELECT * FROM blog WHERE id = ?'
        
        return self.client.query(query, (id,))
    
    def get_many_blogs(self, ids):
        placeholders = ', '.join('?' for _ in ids)
        query = f'SELECT * FROM blog WHERE id IN ({placeholders})'
        return self.client.query(query, ids)
    
    def delete_blog(self, id):
        query = 'DELETE FROM blog WHERE id = ?'
        self.client.query(query, (id,))
        return self.client.cursor.rowcount
    
    def delete_many_blogs(self, ids):
        placeholders = ', '.join('?' for _ in ids)
        query = f'DELETE FROM blog WHERE id IN ({placeholders})'
        self.client.query(query, ids)
        return self.client.cursor.rowcount
    
    def update_blog(self, blog_data):
        fields = []
        values = []
        
        if "title" in blog_data:
            fields.append("title = ?")
            values.append(blog_data["title"])
        if "content" in blog_data:
            fields.append("content = ?")
            values.append(blog_data["content"])
        if "tags" in blog_data:
            fields.append("tags = ?")
            values.append(blog_data["tags"])
        if "date" in blog_data:
            fields.append("date = ?")
            values.append(blog_data["date"])
        
        values.append(blog_data["id"])
        
        query = f'UPDATE blog SET {", ".join(fields)} WHERE id = ?'
        self.client.query(query, values)
        return self.client.cursor.rowcount
    
    def update_many_blogs(self, blogs_data):
        rowcount = 0
        for blog_data in blogs_data:
            fields = []
            values = []
            
            if "title" in blog_data:
                fields.append("title = ?")
                values.append(blog_data["title"])
            if "content" in blog_data:
                fields.append("content = ?")
                values.append(blog_data["content"])
            if "tags" in blog_data:
                fields.append("tags = ?")
                values.append(blog_data["tags"])
            if "date" in blog_data:
                fields.append("date = ?")
                values.append(blog_data["date"])
            
            values.append(blog_data["id"])
            
            query = f'UPDATE blog SET {", ".join(fields)} WHERE id = ?'
            self.client.query(query, values)
            rowcount += self.client.cursor.rowcount
        
        return rowcount