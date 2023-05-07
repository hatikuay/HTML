from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\tmp\\test.db'
    db.init_app(app)
    app.app_context().push() # <-- Add this line
    
    from my_app.book_store.views import book_store
    app.register_blueprint(book_store)
    #with app.app_context():
    db.create_all()
    return app
