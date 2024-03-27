from apiflask import Schema, fields

#- PUPIL BOOK SCHEMA
####################

class PupilBookSchema(Schema):
    pupil_id = fields.Integer()
    book_id = fields.String()
    state = fields.String()
    lent_at = fields.Date()
    lent_by = fields.String()
    returned_at = fields.Date()
    received_by = fields.String()
    class Meta:
        fields = ('pupil_id', 'book_id', 'state', 'lent_at', 'lent_by',
                  'returned_at', 'received_by' )

pupil_book_schema = PupilBookSchema()
pupil_books_schema = PupilBookSchema(many=True)

class PupilBookListSchema(Schema):
    pupil_id = fields.Integer()
    state = fields.String()
    lent_at = fields.Date()
    lent_by = fields.String()
    returned_at = fields.Date()
    received_by = fields.String()    
    class Meta:
        fields = ('pupil_id', 'state', 'lent_at', 'lent_by', 'returned_at', 'received_by' )

pupil_book_list_schema = PupilBookListSchema()
pupil_books_list_schema = PupilBookListSchema(many=True)

#- BOOK SCHEMA
##############

class BookSchema(Schema):
    book_id = fields.String()
    isbn = fields.Integer()
    title = fields.String()
    author = fields.String()
    location = fields.String()
    reading_level = fields.String()
    image_url = fields.String()
    reading_pupils = fields.List(fields.Nested(PupilBookListSchema))
    class Meta:
        fields = ('book_id', 'isbn', 'title', 'author', 'location', 
                  'reading_level', 'image_url','reading_pupils')

book_schema = BookSchema()
books_schema = BookSchema(many=True)

class BookFlatSchema(Schema):
    book_id = fields.String()
    isbn = fields.Integer()
    title = fields.String()
    author = fields.String()
    location = fields.String()
    reading_level = fields.String()
    image_url = fields.String()
    class Meta:
        fields = ('book_id', 'isbn', 'title', 'author', 'location', 
                  'reading_level', 'image_url')

book_flat_schema = BookFlatSchema()
books_flat_schema = BookFlatSchema(many=True)
