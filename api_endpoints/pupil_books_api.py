from datetime import datetime
from models.pupil import Pupil
from models.book import Book, PupilBook
from schemas.book_schemas import *
from sqlalchemy.sql import exists
from apiflask import APIBlueprint
from flask import jsonify, request
from app import db
from auth_middleware import token_required

pupil_book_api = APIBlueprint('pupil_book_api', __name__, url_prefix='/api/pupil_book')

#- POST PUPIL BOOK
##################
@pupil_book_api.route('/<internal_id>/book/<book_id>', methods=['POST'])
@pupil_book_api.doc(security='ApiKeyAuth', tags=['Pupil Books'])
@token_required
def add_book_to_pupil(current_user, internal_id, book_id):
    this_pupil = Pupil.query.filter_by(internal_id = internal_id).first()
    if this_pupil == None:
        return jsonify({'error': 'This pupil does not exist!'}), 404
    pupil_id = internal_id
    this_book = Book.query.filter_by(book_id = book_id).first()
    if this_book == None:
        return jsonify({'error': 'This book does not exist!'}), 401    
    if db.session.query(exists().where(PupilBook.book_id == book_id and PupilBook.pupil_id == internal_id and PupilBook.returned_at != None)).scalar() == True:
        return jsonify({'error': 'This pupil book exists already!'})    
    state = 'active' 
    lent_by = current_user.name
    now = datetime.strptime(datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    lent_at =  now
    returned_at = None
    received_by = None   
    new_pupil_book = PupilBook(pupil_id, book_id, state, lent_at, lent_by, returned_at, received_by)
    db.session.add(new_pupil_book)
    db.session.commit()
    return pupil_book_schema.jsonify(new_pupil_book)

#- PATCH PUPIL BOOK  
###################
@pupil_book_api.route('/<internal_id>/<book_id>', methods=['PATCH'])
@pupil_book_api.doc(security='ApiKeyAuth', tags=['Pupil Books'], summary='Patch a pupil book')
@token_required
def update_PupilBook(current_user, internal_id, book_id):
    pupil_book = PupilBook.query.filter_by(pupil_id = internal_id,                                                 book_id = book_id).first()
    if pupil_book == None:
        return jsonify({'error': 'This pupil book does not exist!'})
    data = request.get_json()
    for key in data:
        match key:
            case 'state':
                pupil_book.state = data[key]
            case 'returned_at':
                pupil_book.returned_at = data[key]
            case 'received_by':
                pupil_book.received_by = data[key]
    db.session.commit()
    return pupil_book_list_schema.jsonify(pupil_book)

#- DELETE PUPIL BOOK
####################
@pupil_book_api.route('/<internal_id>/<book_id>', methods=['DELETE'])
@pupil_book_api.doc(security='ApiKeyAuth', tags=['Pupil Books'], summary='delete a pupil book')
@token_required
def delete_PupilBook(current_user, internal_id, book_id):
    # if not current_user.admin:
    #     return jsonify({'message' : 'Not authorized!'})
    this_book = PupilBook.query.filter_by(pupil_id = internal_id,                                                 book_id = book_id).first()
    db.session.delete(this_book)
    db.session.commit()
    return jsonify( {"message": "Das ausgeliehene Buch wurde gelöscht!"}), 200
