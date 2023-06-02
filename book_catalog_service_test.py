import os
from my_app import app, db
from my_app.book_store.models import Book
import unittest
import tempfile


class BookCatalogServiceTest(unittest.TestCase):
    def setUp(self):
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            self.test_db_file
        app.config['TESTING'] = True
        self.app = app.test_client()
        
        
        if "sqlalchemy" not in app.extensions:
            db.init_app(app)
            app.app_context().push()  # <-- Add this line
            db.create_all()
                   
            from my_app.book_store.book_catalog_service import book_catalog_service
            app.register_blueprint(book_catalog_service)

            book1 = Book(title="Book1", publication_year=2021, author="Author1")
            book2 = Book(title="Book2", publication_year=2022, author="Author2")
            book3 = Book(title="Book3", publication_year=2023, author="Author3")

            db.session.add(book1)
            db.session.add(book2)
            db.session.add(book3)
            db.session.commit()
      
    def tearDown(self) -> None:
        # os.remove(self.test_db_file)
        pass

    def test_get_all_books(self):
        response = self.app.get("/GET/api/books")
        data = response.get_json()
        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        # Verify that the response data is a list
        self.assertIsInstance(data, list)
        # Assert the number of books in the response
        self.assertEqual(len(data), 4)

    def test_get_book_by_id(self):
        book = Book(title="Test Book", publication_year=2021,
                    author="Ercan Erkalkan")
        db.session.add(book)
        db.session.commit()
        response = self.app.get(f"/GET/api/books?id={book.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["id"], book.id)
        self.assertEqual(data["title"], book.title)
        self.assertEqual(data["publication_year"], book.publication_year)
        self.assertEqual(data["author"], book.author)

    def test_search_book_by_title(self):
        book1 = Book(title="Book1", publication_year=2021, author="Author1")
        book2 = Book(title="Book2", publication_year=2022, author="Author2")
        book3 = Book(title="Book3", publication_year=2023, author="Author3")

        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.commit()
        
        response = self.app.get(f"/GET/api/books?title=Book2")
        data = response.get_json()

        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Verify that the response data is a list
        self.assertIsInstance(data, list)
        
        book = data[0]
        self.assertEqual(book["title"], "Book2")
        self.assertEqual(book["publication_year"], 2022)
        self.assertEqual(book["author"], "Author2")
    
    def test_search_book_by_author(self):
        book1 = Book(title="Book1", publication_year=2021, author="Author1")
        book2 = Book(title="Book2", publication_year=2022, author="Author2")
        book3 = Book(title="Book3", publication_year=2023, author="Author3")

        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.commit()
        
        response = self.app.get(f"/GET/api/books?author=Author2")
        data = response.get_json()

        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Verify that the response data is a list
        self.assertIsInstance(data, list)
        
        book = data[0]
        self.assertEqual(book["title"], "Book2")
        self.assertEqual(book["publication_year"], 2022)
        self.assertEqual(book["author"], "Author2")
    
    def test_search_book_by_publication_year(self):
        book1 = Book(title="Book1", publication_year=2021, author="Author1")
        book2 = Book(title="Book2", publication_year=2022, author="Author2")
        book3 = Book(title="Book3", publication_year=2023, author="Author3")

        db.session.add(book1)
        db.session.add(book2)
        db.session.add(book3)
        db.session.commit()
        
        response = self.app.get(f"/GET/api/books?publication_year=2022")
        data = response.get_json()

        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)
        
        # Verify that the response data is a list
        self.assertIsInstance(data, list)
        
        book = data[0]
        self.assertEqual(book["title"], "Book2")
        self.assertEqual(book["publication_year"], 2022)
        self.assertEqual(book["author"], "Author2")

    def test_delete_book_by_id(self):
        book = Book(title="Test Book", publication_year=2021,
                    author="Ercan Erkalkan")
        db.session.add(book)
        db.session.commit()
        response = self.app.get(f"/DELETE/api/books?id={book.id}")
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["id"], book.id)
        self.assertEqual(data["title"], book.title)
        self.assertEqual(data["publication_year"], book.publication_year)
        self.assertEqual(data["author"], book.author)

    def test_update_book_by_id(self):
        book = Book(title="Test Book", publication_year=2021,
                    author="Ercan Erkalkan")
        db.session.add(book)
        db.session.commit()        
        data = {"title": "In Search of Lost Time",
                "publication_year": 2002,
                "author": "Marcel Proust",
                }
        response = self.app.post(f"/UPDATE/api/books?id={book.id}", data=data)        
        updated_data = response.get_json()

        self.assertEqual(response.status_code, 200)

        self.assertEqual(data["title"], updated_data["title"])
        self.assertEqual(data["publication_year"], updated_data["publication_year"])
        self.assertEqual(data["author"], updated_data["author"])

    def test_create_book(self):
        # Prepare the book data
        book_data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": "New Author"
        }

        # Send a POST request to create the book
        response = self.app.post("/POST/api/books", data=book_data)

        # Verify the response status code is 201 (Created)
        self.assertEqual(response.status_code, 200)

        # Verify that the book is created in the database
        created_book = Book.query.filter_by(title=book_data["title"]).first()
        print(created_book)
        self.assertIsNotNone(created_book)
        self.assertEqual(created_book.title, book_data["title"])
        self.assertEqual(created_book.publication_year, book_data["publication_year"])
        self.assertEqual(created_book.author, book_data["author"])

if __name__ == "__main__":
    unittest.main()
