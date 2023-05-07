from my_app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, publication_year):
        self.title = title
        self.author = author
        self.publication_year = publication_year
    
    def to_dict(self):
        book_dict = {
            "id":self.id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
        }
        return book_dict

    def __repr__(self):
        return f'<Book {self.title}>'
