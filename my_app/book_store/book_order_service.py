from my_app import db
from flask import Flask, render_template, request, redirect, url_for, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from my_app.book_store.models import Book, Inventory, BookOrder

book_order_service = Blueprint('book_order_service', __name__)

@book_order_service.route("/api/books/orders", methods = ["POST"])
def api_books_orders():
    data = request.json
    book_id = data.get("book_id")
    quantity_ordered = data.get("quantity_ordered")
    
    order = BookOrder(book_id=book_id,quantity_ordered=quantity_ordered)
    order.save()
    
    response = {"message": "Order placed successfully."}
    return jsonify(response), 201

