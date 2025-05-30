from flask import *
from app.application import app
import json


class Database:
    def __init__(self):
        with open('db.json', 'r') as file:
            self.db = json.load(file)
        self.last_id = max([int(book["id"]) for book in self.db["books"]], default=0)

    def get_db(self):
        return self.db

    def return_books(self):
        return self.db["books"]

    def return_book(self, id):
        for book in self.db["books"]:
            if book["id"] == str(id):
                return book
        return None

    def return_users(self):
        return self.db["users"]

    def return_user(self, id):
        return self.db["users"][int(id)]

    def create_book(self, title, author, isbn):
        self.last_id += 1
        new_book = {
            "id": str(self.last_id),
            "title": title,
            "author": author,
            "isbn": isbn,
            "is_reserved": False,
            "reserved_by": None
        }
        self.db["books"].append(new_book)
        with open('db.json', 'w') as file:
            json.dump(self.db, file, indent=4)
        return new_book


@app.route("/api/v1/books", methods=["GET"])
def get_books():
    books_info = Database().return_books()
    return jsonify(books_info)


@app.route("/api/v1/books/<book_id>", methods=["GET"])
def get_book(book_id: str):
    book_info = Database().return_book(book_id)
    if book_info:
        return jsonify(book_info)
    return jsonify({"error": "Book not found"}), 404


@app.route("/api/v1/books", methods=["POST"])
def create_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    isbn = data.get("isbn")
    new_book = Database().create_book(title, author, isbn)
    return jsonify(new_book), 201


@app.route("/api/v1/books/<book_id>", methods=["DELETE"])
def delete_book(book_id: str):
    db = Database()
    books = db.return_books()
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(i)
            with open('db.json', 'w') as file:
                json.dump(db.get_db(), file, indent=4)
            return jsonify({"message": "Book deleted successfully"})
    return jsonify({"error": "Book not found"}), 404
