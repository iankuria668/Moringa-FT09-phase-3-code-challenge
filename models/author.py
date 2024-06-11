from models import get_db_connection
class Author:
    def __init__(self, id=None, name=None):
        if id:
            self._id = id
            self._name = self._fetch_name_by_id(id)
        elif name:
            self._id = self._insert_author(name)
            self._name = name
        else:
            raise ValueError('Either id or name must be provided.')

    def _insert_author(self, name):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO authors (name) VALUES (?)', (name,))
            conn.commit()
            return cursor.lastrowid
        

    def _fetch_name_by_id(self, id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id = ?', (id,))
            result = cursor.fetchone()
            if result is None:
                raise ValueError(f'Author with id {id} does not exist.')
            return result['name']

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, name):
        if 2 <= len(name) <= 100:
            self._name = name
        else:
            raise ValueError('Name must be between 2 and 100 characters')

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
            articles = cursor.fetchall()
            return articles

    def magazines(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id IN (SELECT magazine_id FROM articles WHERE author_id = ?)', (self.id,))
            magazines = cursor.fetchall()
            return magazines

    def __repr__(self):
        return f'<Author {self.name}>'
