from my_app import db
from flask import Flask, render_template, request, redirect, url_for, request, jsonify, Blueprint
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from my_app.book_store.models import Book, Inventory, BookOrder

book_catalog_service = Blueprint('book_catalog_service', __name__)

@book_catalog_service.route("GET/api/books")
def read():
    #id = request.args.get("id")
    if id:
        book = Book.query.get(id)
        return jsonify(book.to_dict())

    title = request.args.get("title")
    publication_year = request.args.get("publication_year")
    author = request.args.get("author")

    if title or publication_year or author:
        books = []
        if title:
            books += Book.query.filter_by(title=title)
        if publication_year:
            books += Book.query.filter_by(publication_year=publication_year)
        if author:
            books += Book.query.filter_by(author=author)
        
        books_list = []
        for book in books:
            books_list.append(book.to_dict())
        return jsonify(books_list)

    books = Book.query.all()
    books_list = []
    for book in books:
        books_list.append(book.to_dict())
    return jsonify(books_list)


@book_catalog_service.route("DELETE/api/books")
def api_books_delete():
    id = request.args.get("id")
    if id:
        book = Book.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify(book.to_dict())
        else:
            return jsonify({"message": "not found"})
    else:
        return jsonify({"message": "no ID given"})

@book_catalog_service.route("POST/api/books", methods = ["POST"])
def api_books_create():
    title = request.form.get("title")
    publication_year = request.form.get("publication_year")
    author = request.form.get("author")
       
    if title and publication_year and author:
        """new_book = Book(
            title=title,
            publication_year=publication_year,
            author=author
        ) 
        db.session.add(new_book)
        db.session.commit()"""
        return jsonify(Book.create_book(title=title,
            publication_year=publication_year,
            author=author))#new_book.to_dict())
    return jsonify({"message": "data missing"})

@book_catalog_service.route("UPDATE/api/books", methods = ["POST"])
def api_books_update():
    id = request.args.get("id")
    if id:
        book = Book.query.get(id)
        if book:
            book.title = request.form.get("title", book.title)
            book.release_year = request.form.get("publication_year", book.publication_year)
            book.author = request.form.get("author", book.author)
            book.inventory = request.form.get("author", book.inventory)
            db.session.commit()
            return jsonify(book.to_dict())
        return jsonify({"message": "not found"})
    return jsonify({"message": "no ID sent"})