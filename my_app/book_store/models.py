from my_app import db
from datetime import datetime


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    #inventory_id = db.Column(db.Integer, db.ForeignKey('inventory.id'))
    inventory = db.relationship('Inventory', backref='book', lazy=True)
    book_order = db.relationship('BookOrder', backref='book', lazy=True)

    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def to_dict(self):
        book_dict = {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year
        }
        return book_dict

    @staticmethod
    def create_book(title, author, publication_year):
        new_book = Book(title=title, author=author,
                        publication_year=publication_year)
        db.session.add(new_book)
        db.session.commit()
        initial_inventory = Inventory(
            book=new_book, quantity=0, available_quantity=0)
        db.session.add(initial_inventory)
        db.session.commit()
        return new_book.to_dict()

    def __repr__(self):
        return f'<Book {self.title}>'


class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, book, quantity, available_quantity):
        self.book = book
        self.quantity = quantity
        self.available_quantity = available_quantity

    def to_dict(self):
        inventory_dict = {
            "id": self.id,
            "book_id": self.book_id,
            "quantity": self.quantity,
            "available_quantity": self.available_quantity,
        }
        return inventory_dict

    def update_available_quantity(self, quantity):
        self.available_quantity += quantity
        db.session.commit()

    def __repr__(self):
        return f'<Inventory {self.available_quantity}>'


class BookOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    quantity_ordered = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, book:Book, quantity_ordered):
        self.book = book
        self.quantity_ordered = quantity_ordered

    def save(self):
        pass

    def delete(self):
        inventory = self.book.inventory
        if inventory:
            inventory.quantity -= self.quantity_ordered
            db.session.delete(self)
            db.session.commit()

    def to_dict(self):
        book_order_dict = {
            "id": self.id,
            "book_id": self.book_id,
            "quantity_ordered": self.quantity_ordered,
            "order_date": self.order_date
        }
        return book_order_dict
