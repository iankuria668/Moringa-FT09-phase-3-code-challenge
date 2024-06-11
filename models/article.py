from models import get_db_connection
class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        if id:
            self.id = id
            self.title = title
            self.content = content
            self.author_id = author_id
            self.magazine_id = magazine_id
        else:
            self.id = id
            self.title = title
            self.content = content
            self.author_id = author_id
            self.magazine_id = magazine_id

    def _insert_article(self, title, content, author_id, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?,?,?,?)', (title, content, author_id, magazine_id))
        conn.commit()
        article_id = cursor.lastrowid
        conn.close()
        return article_id
    
    def fetch_details_by_id(self, id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE id = ?', (id,))
        article = cursor.fetchone()
        conn.close()
        return article
    
    @property
    def id(self):
        return self._id
    
    @property
    def title(self):
        return self._title
    
    @property
    def content(self):
        return self._content
    
    @property
    def author_id(self):
        return self._author_id
    
    @property
    def magazine_id(self):
        return self._magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'
