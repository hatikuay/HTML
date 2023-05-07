from my_app import db, app
from my_app.book_store.models import Book

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\tmp\\book.db'
db.init_app(app)
app.app_context().push() # <-- Add this line

db.create_all()

book1 = Book(title="The Adventures of Huckleberry Finn", publication_year=2004,
             author="Mark Twain")
book2 = Book(title="The Great Gatsby", publication_year=2004,
             author="Scott Fitzgerald")
book3 = Book(title="Anna Karenina", publication_year=2009,
             author="Leo Tolstoy")
book4 = Book(title="Madame Bovary", publication_year=1992,
             author="Gustave Flaubert")


db.session.add(book1)
db.session.add(book2)
db.session.add(book3)
db.session.add(book4)

db.session.commit()
