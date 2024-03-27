from apiflask import Schema, fields
from apiflask.fields import File, String, Integer

from schemas.admonition_schemas import AdmonitionSchema
from schemas.missed_class_schemas import MissedClassNoMissedDaySchema


class SchooldaySchema(Schema):
    schoolday = fields.String()
    missed_classes = fields.List(fields.Nested(MissedClassNoMissedDaySchema))
    admonitions = fields.List(fields.Nested(AdmonitionSchema))
    class Meta:
        fields = ('schoolday', 'missed_classes', 'admonitions')

schoolday_schema = SchooldaySchema()
schooldays_schema = SchooldaySchema(many = True)

class SchooldayOnlySchema(Schema):
    schoolday = fields.String()
    class Meta:
        fields = ('schoolday',)

schoolday_only_schema = SchooldayOnlySchema()
schooldays_only_schema = SchooldayOnlySchema(many = True)

##########################
#- SCHOOL SEMESTER SCHEMA
##########################

class SchoolSemesterSchema(Schema):
    start_date = fields.Date()
    end_date = fields.Date()
    is_first = fields.Boolean()
    class Meta:
        fields = ('start_date', 'end_date', 'is_first')

school_semester_schema = SchoolSemesterSchema()
school_semesters_schema = SchoolSemesterSchema(many=True)
