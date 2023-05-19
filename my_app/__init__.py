from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\tmp\\book.db'
    db.init_app(app)
    app.app_context().push() # <-- Add this line
    
    #from my_app.book_store.views import book_store
    from my_app.book_store.book_catalog_service import book_catalog_service
    from my_app.book_store.book_order_service import book_order_service
    from my_app.book_store.book_inventory_service import book_inventory_service
    
    app.register_blueprint(book_catalog_service)
    app.register_blueprint(book_order_service)
    app.register_blueprint(book_inventory_service)
    
    #with app.app_context():
    db.create_all()
    return app
