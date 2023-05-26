import os 
from my_app import app, db 
import unittest 
import tempfile

from my_app import app, db


class BookCatalogServiceTest(unittest.TestCase):
    def setUp(self):
        self.test_db_file = tempfile.mkstemp()[1] 
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file 
        app.config['TESTING'] = True 
        self.app = app.test_client()
        db.init_app(app)
        app.app_context().push() # <-- Add this line 
        db.create_all()

    def tearDown(self) -> None:
        os.remove(self.test_db_file)

    def test_get_all_books(self):
        books = self.app.get("GET/api/books")
        self.assertEqual(len(books), 3)

    """def test_get_book_by_id(self):
        pass
    
    def test_search_book_by_title(self):
        pass
    
    def test_search_book_by_author(self):
        pass
    
    def test_search_book_by_publication_year(self):
        pass

    def test_delete_book_by_id(self):
        pass
    
    def test_update_book_by_id(self):
        pass
    
    def test_create_book(self):
        pass"""


if __name__ == "__main__":
    unittest.main()
