from my_app import db
from flask import Flask, render_template, request, redirect, url_for, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from my_app.book_store.models import Book, Inventory, BookOrder

book_inventory_service = Blueprint('book_inventory_service', __name__)

@book_inventory_service.route("/GET/api/books/inventory")
def get_inventory():
    book_id = request.args.get("book_id")
    if book_id:
        inventory:Inventory = Inventory.query.filter_by(book_id=book_id).first()
        if inventory:
            return jsonify(inventory.to_dict())
        else:
            return jsonify({"message": "Inventory not found for given book ID."})
    else:
        inventories = Inventory.query.all()
        inventories_list = [inventory.to_dict() for inventory in inventories]
        return jsonify(inventories_list)

@book_inventory_service.route("/UPDATE/api/books/inventory", methods = ["POST"])
def update_inventory():
    book_id = request.form.get("book_id")
    quantity = request.form.get("quantity")
    if book_id and quantity:
        inventory:Inventory = Inventory.query.filter_by(book_id=book_id).first()
        if inventory:
            inventory.quantity = quantity
        else:
            inventory:Inventory = Inventory(book_id=book_id, quantity=quantity, available_quantity=quantity)
            db.session.add(inventory)
        db.session.commit()
        return jsonify(inventory.to_dict())
    else:
        return jsonify({"message": "Invalid request. Book ID and stock count are required"}) 



