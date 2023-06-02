import unittest
from my_app import app, db
from my_app.book_store.models import Book, Inventory, BookOrder
import tempfile


class BookOrderServiceTest(unittest.TestCase):
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

            from my_app.book_store.book_inventory_service import book_inventory_service
            app.register_blueprint(book_inventory_service)
            from my_app.book_store.book_catalog_service import book_catalog_service
            app.register_blueprint(book_catalog_service)
            from my_app.book_store.book_order_service import book_order_service
            app.register_blueprint(book_order_service)

            book1 = Book(title="Book1", publication_year=2021,
                         author="Author1")
            book2 = Book(title="Book2", publication_year=2022,
                         author="Author2")
            book3 = Book(title="Book3", publication_year=2023,
                         author="Author3")

            db.session.add(book1)
            db.session.add(book2)
            db.session.add(book3)
            db.session.commit()

            inventory1 = Inventory(
                book=book1, quantity=2, available_quantity=2)
            inventory2 = Inventory(
                book=book2, quantity=2, available_quantity=2)
            inventory3 = Inventory(
                book=book3, quantity=2, available_quantity=2)

            db.session.add(inventory1)
            db.session.add(inventory2)
            db.session.add(inventory3)
            db.session.commit()
            
    def tearDown(self) -> None:
        return super().tearDown()

    def test_create_book_order(self):
        # Prepare the book order data
        book_order_data = {
            "book_id": 1,
            "quantity_ordered": 2
        }

        # Send a POST request to create the book order
        response = self.app.post("/POST/api/books/orders", data=book_order_data)
        data = response.get_json()
        print(data)

        # Verify the response status code is 201 (Created)
        self.assertEqual(response.status_code, 201)

        # Verify the response message
        self.assertEqual(data["message"], "Order placed successfully.")

if __name__ == "__main__":
    unittest.main()
