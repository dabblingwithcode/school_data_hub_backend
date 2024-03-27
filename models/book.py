from models.schoolday import *

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    book_id = db.Column(db.String(50), nullable = False, unique = True)
    isbn = db.Column(db.Integer, nullable = False)
    title = db.Column(db.String(50))
    author = db.Column(db.String(20))
    location = db.Column(db.String(20))
    reading_level = db.Column(db.String(10))
    image_url = db.Column(db.String(50), unique=True, nullable = True)

    #- RELATIONSHIP TO PUPIL BOOKS ONE-TO-MANY
    reading_pupils = db.relationship('PupilBook', back_populates='book',
                                     cascade='all, delete-orphan')

    def __init__(self, book_id, isbn, title, author, location, reading_level, image_url):
        self.book_id = book_id
        self.isbn = isbn
        self.title = title
        self.author = author
        self.location = location
        self.reading_level = reading_level
        self.image_url = image_url
 
## many to many & association proxy: https://youtu.be/IlkVu_LWGys

class PupilBook(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    state = db.Column(db.String(10), nullable = True)
    lent_at = db.Column(db.Date, nullable = False)
    lent_by = db.Column(db.String(20),nullable = False)
    returned_at = db.Column(db.Date, nullable = True)
    received_by = db.Column(db.String(20),nullable = True)

    #- RELATIONSHIP TO PUPIL MANY-TO-ONE
    pupil_id = db.Column('pupil_id', db.Integer, db.ForeignKey('pupil.internal_id'))
    pupil = db.relationship('Pupil', back_populates='pupil_books')

    #- RELATIONSHIP TO BOOK MANY-TO-ONE
    book_id = db.Column('book_id', db.String(50), db.ForeignKey('book.book_id'))
    book = db.relationship('Book', back_populates='reading_pupils')

    def __init__(self, pupil_id, book_id, state,
                 lent_at, lent_by, returned_at, received_by):
        self.pupil_id = pupil_id
        self.book_id = book_id
        self.state = state
        self.lent_at = lent_at
        self.lent_by = lent_by
        self.returned_at = returned_at
        self.received_by = received_by