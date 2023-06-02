from my_app import db
from flask import Flask, render_template, request, redirect, url_for, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from my_app.book_store.models import Book, Inventory, BookOrder

book_order_service = Blueprint('book_order_service', __name__)

@book_order_service.route("/POST/api/books/orders", methods = ["POST"])
def api_books_orders():
    book_id = request.form.get("book_id")
    book = Book.query.get(book_id)
    quantity_ordered = request.form.get("quantity_ordered")
    if book_id and quantity_ordered:
        order = BookOrder(book=book,quantity_ordered=quantity_ordered)
        #order.save()
        response = {"message": "Order placed successfully."}
        return jsonify(response), 201
    else:
        response = {"message": "data missing"}
        return jsonify(response), 201


