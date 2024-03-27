from apiflask import Schema, fields

########################
#- PUPIL WORKBOOK SCHEMA
########################

class PupilWorkbookSchema(Schema):
    workbook_isbn = fields.Integer()
    state = fields.String(allow_none = True)
    created_by = fields.String()
    created_at = fields.Date()
    finished_at = fields.Date(allow_none = True)
    class Meta:
        fields = ('workbook_isbn', 'state', 'created_by', 'created_at', 'finished_at' )

pupil_workbook_schema = PupilWorkbookSchema()
pupil_workbooks_schema = PupilWorkbookSchema(many=True)

class PupilWorkbookListSchema(Schema):
    pupil_id = fields.Integer()
    state = fields.String()
    created_by = fields.String()
    created_at = fields.Date()
    finished_at = fields.Date(allow_none = True)
    class Meta:
        fields = ('pupil_id', 'state', 'created_by', 'created_at', 'finished_at' )

pupil_workbook_list_schema = PupilWorkbookListSchema()
pupil_workbooks_list_schema = PupilWorkbookListSchema(many=True)

###################
#- WORKBOOK SCHEMA
###################

class WorkbookSchema(Schema):
    isbn = fields.Integer()
    name = fields.String()
    subject = fields.String()
    level = fields.String()
    image_url = fields.String(allow_none = True)
    working_pupils = fields.List(fields.Nested(PupilWorkbookListSchema))
    class Meta:
        fields = ('isbn', 'name', 'subject', 'level','image_url','working_pupils')

workbook_schema = WorkbookSchema()
workbooks_schema = WorkbookSchema(many=True)

class WorkbookFlatSchema(Schema):
    isbn = fields.Integer()
    name = fields.String()
    subject = fields.String()
    level = fields.String()
    image_url = fields.String()   
    class Meta:
        fields = ('isbn', 'name', 'subject', 'level', 'image_url')

workbook_flat_schema = WorkbookFlatSchema()
workbooks_flat_schema = WorkbookFlatSchema(many=True)
