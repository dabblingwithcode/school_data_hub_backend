from apiflask import Schema, fields, abort
from apiflask.fields import File, String, Integer

class MissedClassInSchema(Schema):
    missed_pupil_id = fields.Integer()
    missed_day = fields.Date()
    missed_type = fields.String()
    excused = fields.Boolean()
    contacted = fields.String(allow_none=True)
    returned = fields.Boolean(allow_none=True)
    written_excuse = fields.Boolean(allow_none=True)
    minutes_late = fields.Integer(allow_none=True)
    returned_at = fields.String(allow_none=True)
    class Meta:
        fields = ( 'missed_pupil_id', 'missed_day', 'missed_type',
                  'excused', 'contacted', 'returned', 'written_excuse', 'minutes_late',
                  'returned_at',)

missed_class_in_schema = MissedClassInSchema()
missed_classes_in_schema = MissedClassInSchema(many = True)

class MissedClassSchema(Schema):
    missed_pupil_id = fields.Integer()
    missed_type = fields.String()
    excused = fields.Boolean()
    contacted = fields.String(allow_none=True)
    returned = fields.Boolean(allow_none=True)
    written_excuse = fields.Boolean(allow_none=True)
    minutes_late = fields.Integer(allow_none=True)
    returned_at = fields.String(allow_none=True)
    created_by = fields.String()
    modified_by = fields.String(allow_none=True)
    include_fk = True
    missed_day: String = fields.Pluck('SchooldaySchema', 'schoolday')
    class Meta:
        fields = ( 'missed_pupil_id', 'missed_day', 'missed_type',
                  'excused', 'contacted', 'returned', 'written_excuse', 'minutes_late',
                  'returned_at', 'created_by', 'modified_by')

missed_class_schema = MissedClassSchema()
missed_classes_schema = MissedClassSchema(many = True)

class MissedClassNoMissedDaySchema(Schema):
    missed_pupil_id = fields.Integer()
    missed_type = fields.String()
    excused = fields.Integer()
    contacted = fields.Integer()
    returned = fields.Integer()
    written_excuse = fields.Integer()
    minutes_late = fields.Integer()
    returned_at = fields.String()
    created_by = fields.String()
    modified_by = fields.String()
    class Meta:
        fields = ( 'missed_pupil_id', 'missed_type',
                  'excused', 'contacted', 'returned', 'written_excuse', 'minutes_late',
                  'returned_at', 'created_by', 'modified_by')

missed_class_no_missed_day_schema = MissedClassNoMissedDaySchema()
missed_classes_no_missed_day_schema = MissedClassNoMissedDaySchema(many = True)

