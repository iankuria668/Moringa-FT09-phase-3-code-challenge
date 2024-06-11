from models import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category=None):
        self._id = None
        self._name = None
        self._category = None

        if id:
            self._id = id
            self._name, self._category = self._fetch_details_by_id(id)
        elif name and category:
            self._id = self._insert_magazine(name, category)
            self._name = name
            self._category = category
        else:
            raise ValueError('Either id or (name and category) must be provided.')

    def _insert_magazine(self, name, category):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO magazines (name, category) VALUES (?,?)', (name, category))
            conn.commit()
            return cursor.lastrowid
    
    def _fetch_details_by_id(self, id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
            magazine = cursor.fetchone()
            if magazine is None:
                raise ValueError(f'Magazine with id {id} does not exist.')
            return magazine['name'], magazine['category']
    
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
    
    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, category):
        if 2 <= len(category) <= 100:
            self._category = category
        else:
            raise ValueError('Category must be between 2 and 100 characters')
        
    def articles(self):
        from models import Article
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE magazine_id = ?', (self.id,))
            articles = cursor.fetchall()
            return [Article(*article) for article in articles]
    
    def contributors(self):
        from models import Author
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM authors WHERE id IN (SELECT author_id FROM articles WHERE magazine_id = ?)', (self.id,))
            authors = cursor.fetchall()
            return [Author(*author) for author in authors]
    
    def article_titles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT title FROM articles WHERE magazine_id = ?', (self.id,))
            titles = cursor.fetchall()
            return [title[0] for title in titles]
    
    def contributing_authors(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT name FROM authors WHERE id IN (SELECT author_id FROM articles WHERE magazine_id = ?)', (self.id,))
            names = cursor.fetchall()
            return [name[0] for name in names]

    def __repr__(self):
        return f'<Magazine {self.name}>'
