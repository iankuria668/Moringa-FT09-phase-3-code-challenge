from models import get_db_connection

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if id:
            self._id = id
            details = self.fetch_details_by_id(id)
            self._title = details['title']
            self._content = details['content']
            self._author_id = details['author_id']
            self._magazine_id = details['magazine_id']
        elif title and content and author_id and magazine_id:
            self._id = self._insert_article(title, content, author_id, magazine_id)
            self._title = title
            self._content = content
            self._author_id = author_id
            self._magazine_id = magazine_id
        else:
            raise ValueError('Either id or (title, content, author_id, magazine_id) must be provided.')

    def _insert_article(self, title, content, author_id, magazine_id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?,?,?,?)', (title, content, author_id, magazine_id))
            conn.commit()
            return cursor.lastrowid
    
    def fetch_details_by_id(self, id):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM articles WHERE id = ?', (id,))
            article = cursor.fetchone()
            if article is None:
                raise ValueError(f'Article with id {id} does not exist.')
            return article
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, title):
        if 2 <= len(title) <= 200:
            self._title = title
        else:
            raise ValueError('Title must be between 2 and 200 characters')

    @property
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        if content:
            self._content = content
        else:
            raise ValueError('Content cannot be empty')
    
    @property
    def author_id(self):
        return self._author_id
    
    @property
    def magazine_id(self):
        return self._magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
