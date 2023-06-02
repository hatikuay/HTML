import unittest
from my_app.book_store.book_inventory_service import book_inventory_service
import os
from my_app import app, db
from my_app.book_store.models import Book, Inventory
import unittest
import tempfile


class BookInventoryServiceTest(unittest.TestCase):
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
        # return super().tearDown()
        pass

    def test_get_book_inventory_by_id(self):
        book_id = 2
        expected_inventory = 2

        # Call the method to get the book inventory by ID
        inventory = self.app.get(f"/GET/api/books/inventory?book_id={book_id}")
        data = inventory.get_json()

        # Verify the response status code is 200
        self.assertEqual(inventory.status_code, 200)

        # Verify that the retrieved inventory matches the expected value
        self.assertEqual(data["available_quantity"], expected_inventory)

    def test_get_book_all_inventory(self):
        # Call the method to get all book inventories
        inventory = self.app.get("/GET/api/books/inventory")
        data = inventory.get_json()

        # Verify the response status code is 200
        self.assertEqual(inventory.status_code, 200)

        # Verify that the response data is a list
        self.assertIsInstance(data, list)

        # Implement additional assertions as per your requirements

    def test_update_book_inventory_by_id(self):
        book_id = 2
        updated_quantity = 10
        data = {"book_id": book_id,
                "quantity": updated_quantity
                }

        # Call the method to update the book inventory by ID
        response = self.app.post(f"/UPDATE/api/books/inventory", data=data)
        data = response.get_json()
        print(data)

        # Verify the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Verify that the updated inventory matches the expected value
        self.assertEqual(data["quantity"], updated_quantity)


if __name__ == "__main__":
    unittest.main()
