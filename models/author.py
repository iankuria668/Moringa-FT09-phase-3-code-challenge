from models import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if id:
            self.id = id
            self.name = self._fetch_name_by_id(id)
        else:
            self.id = id
            self.name = name._insert_author(name)

    def _insert_author(self, name):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
        conn.commit()
        author_id = cursor.lastrowid
        conn.close()
        return author_id

    def _fetch_name_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM authors WHERE id = ?', (id,))
        name = cursor.fetchone()[0]
        conn.close()
        return name
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    def articles(self):
        from models import Article
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return articles
    
    def magazines(self):
        from models import Magazine
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id IN (SELECT magazine_id FROM articles WHERE author_id = ?)', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return magazines

    def __repr__(self):
        return f'<Author {self.name}>'
