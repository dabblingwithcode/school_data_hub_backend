import os
import uuid
from models.book import Book
from schemas.book_schemas import *
from apiflask import APIBlueprint, abort
from flask import current_app, jsonify, request
from app import db
from auth_middleware import token_required

book_api = APIBlueprint('book_api', __name__, url_prefix='/api/book')

#- GET BOOKS
############
@book_api.route('/all', methods=['GET'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'], summary='get all books including reading pupils')
@token_required
def get_books(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_books = Book.query.all()
    if all_books == []:
        return jsonify({'message': 'No books found!'}), 404
    result = books_schema.dump(all_books)
    return jsonify(result)

#- GET BOOKS FLAT
#################
@book_api.route('/all/flat', methods=['GET'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'], summary='get all books without nested elements')
@token_required
def get_books_flat(current_user):
    if not current_user:
        abort(404, message='Bitte erneut einloggen!')
    all_books = Book.query.all()
    if all_books == []:
        return jsonify({'message': 'No books found!'}), 404
    result = books_flat_schema.dump(all_books)
    return jsonify(result)

#- POST BOOK 
############
@book_api.route('/new', methods=['POST'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'])
@token_required
def create_book(current_user):
    book_id = request.json['book_id']
    if db.session.query(Book).filter_by(book_id= book_id).scalar() is not None:
        return jsonify({"message": "This book already exists!"}), 400
    isbn = request.json['isbn']
    location = request.json['location']
    title = request.json['title']
    author = request.json['author']
    reading_level = request.json['reading_level']
    image_url = request.json['image_url']
    new_book = Book(book_id, isbn, title, author, location, reading_level, image_url)
    db.session.add(new_book)
    db.session.commit()
    return book_schema.jsonify(new_book)

#- PATCH BOOK 
#############
@book_api.route('/<book_id>', methods=['PATCH'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'], summary='Patch an existing book')
@token_required
def patch_book(current_user, book_id):
    book = db.session.query(Book).filter_by(book_id= book_id).scalar()
    if book is None:
        return jsonify({'message': 'Das Buch existiert nicht!'}), 404
    data = request.get_json()
    for key in data:
        match key:
            case 'title':
                book.title = data['title']
            case 'author':
                book.author = data['author']
            case 'location':
                book.location = data['location']
            case 'reading_level':
                book.reading_level = data['reading_level']
            case 'image_url':
                book.image_url = data['image_url']
    db.session.commit()
    return book_flat_schema.jsonify(book)

#- PATCH BOOK FILE
##################
@book_api.route('/<book_id>/file', methods=['PATCH'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'], summary='PATCH-POST a file for a given book')
@token_required
def upload_book_file(current_user, book_id):
    book = db.session.query(Book).filter_by(book_id= book_id).scalar()
    if book is None:
        return jsonify({'message': 'Das Buch existiert nicht!'}), 404
    if 'file' not in request.files:
        return jsonify({'error': 'No file attached!'}), 400
    file = request.files['file']   
    filename = str(uuid.uuid4().hex) + '.jpg'
    file_url = current_app.config['UPLOAD_FOLDER'] + '/book/' + filename
    file.save(file_url)
    if len(str(book.image_url)) > 4:
        os.remove(str(book.image_url))
    book.image_url = file_url
    db.session.commit()
    return book_schema.jsonify(book)

#- DELETE BOOK 
##############
@book_api.route('/<book_id>', methods=['DELETE'])
@book_api.doc(security='ApiKeyAuth', tags=['Books'])
@token_required
def delete_book(current_user, book_id):
    if not current_user.admin:
        return jsonify({'error' : 'Not authorized!'}), 401
    this_book = Book.query.filter_by(book_id = book_id).first()
    if this_book == None:
        return jsonify({'error': 'This book does not exist!'}), 404
    if len(str(this_book.image_url)) > 4:
        os.remove(str(this_book.image_url))
    db.session.delete(this_book)
    db.session.commit()
    return jsonify( {"message": "Book deleted!"}), 200
