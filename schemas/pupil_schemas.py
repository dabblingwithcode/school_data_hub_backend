from apiflask import Schema, fields
from apiflask.fields import String
from schemas.admonition_schemas import AdmonitionSchema
from schemas.authorization_schemas import PupilAuthorizationSchema
from schemas.book_schemas import PupilBookSchema
from schemas.competence_schemas import CompetenceCheckSchema, CompetenceGoalSchema, CompetenceReportSchema
from schemas.credit_schema import CreditHistoryLogSchema
from schemas.goal_schemas import PupilCategoryStatusSchema, PupilGoalSchema
from schemas.missed_class_schemas import MissedClassSchema
from schemas.school_list_schemas import PupilProfileListSchema
from schemas.workbook_schemas import PupilWorkbookSchema

class PupilSchema(Schema):
    avatar_url = fields.String(metadata={'nullable': True})
    internal_id = fields.Integer(metadata={'required': True})
    name = fields.String(required = True)
    contact =  fields.String(metadata={'nullable': True})
    parents_contact = fields.String(metadata={'nullable': True})
    credit = fields.Integer()
    credit_earned = fields.Integer()
    ogs = fields.Boolean()
    pick_up_time = fields.String()
    ogs_info = fields.String()
    individual_development_plan = fields.Integer()
    five_years = fields.String()
    communication_pupil = fields.String(allow_none=True)
    communication_tutor1 = fields.String(allow_none=True)
    communication_tutor2 = fields.String(allow_none=True)
    preschool_revision = fields.Integer()
    pupil_missed_classes = fields.List(fields.Nested(MissedClassSchema))
    pupil_admonitions = fields.List(fields.Nested(AdmonitionSchema))
    pupil_goals = fields.List(fields.Nested(PupilGoalSchema))
    competence_goals = fields.List(fields.Nested(CompetenceGoalSchema))
    pupil_category_statuses = fields.List(fields.Nested(PupilCategoryStatusSchema))
    pupil_workbooks = fields.List(fields.Nested(PupilWorkbookSchema))
    pupil_books = fields.List(fields.Nested(PupilBookSchema))
    pupil_lists = fields.List(fields.Nested(PupilProfileListSchema))
    competence_checks = fields.List(fields.Nested(CompetenceCheckSchema))
    competence_reports = fields.List(fields.Nested(CompetenceReportSchema))
    authorizations = fields.List(fields.Nested(PupilAuthorizationSchema))
    credit_history_logs = fields.List(fields.Nested(CreditHistoryLogSchema))
    class Meta:
        fields = ('internal_id', 'contact', 'parents_contact','credit', 'credit_earned', 'ogs', 'pick_up_time',
                  'ogs_info', 'individual_development_plan', 'five_years', 
                  'communication_pupil', 
                  'communication_tutor1', 'communication_tutor2', 
                  'preschool_revision', 'pupil_missed_classes', 
                  'pupil_admonitions', 'pupil_goals', 'competence_goals', 'pupil_category_statuses', 
                  'pupil_workbooks', 'pupil_books', 'pupil_lists', 'avatar_url', 'special_information', 'authorizations', 'competence_checks', 'competence_reports', 'credit_history_logs')
pupil_schema = PupilSchema()
pupils_schema = PupilSchema(many = True)

class PupilFlatSchema(Schema):
    
    internal_id = fields.Integer()
    contact =  String(allow_none=True)
    parents_contact = String(allow_none=True)
    credit = fields.Integer()
    credit_earned = fields.Integer()
    ogs = fields.Boolean()
    pick_up_time = fields.String(allow_none=True)
    ogs_info = fields.String(allow_none=True)
    individual_development_plan = fields.Integer()
    five_years = fields.String(allow_none=True)
    communication_pupil = fields.String(allow_none=True)
    communication_tutor1 = fields.String(allow_none=True)
    communication_tutor2 = fields.String(allow_none=True)
    preschool_revision = fields.Integer(allow_none=True)
    avatar_url = fields.String(allow_none=True)
    special_information = fields.String(allow_none=True)
    class Meta:
        fields = ('internal_id', 'contact', 'parents_contact','credit', 
                  'credit_earned', 'ogs', 'pick_up_time', 'ogs_info', 
                  'individual_development_plan', 'five_years', 
                   'communication_pupil', 'communication_tutor1', 
                   'communication_tutor2', 'preschool_revision', 
                   'avatar_url', 'special_information')

pupil_flat_schema = PupilFlatSchema()
pupils_flat_schema = PupilFlatSchema(many = True)

class PupilOnlyGoalSchema(Schema):
    internal_id = fields.String()   
    pupil_goals = fields.List(fields.Nested(PupilGoalSchema))    
    class Meta:
        fields = ('internal_id', 'pupil_goals')

pupil_only_goal_schema = PupilOnlyGoalSchema()
pupils_only_goal_schema = PupilOnlyGoalSchema(many = True)

class PupilIdListSchema(Schema):
    pupils = fields.List(fields.Integer())
pupil_id_list_schema = PupilIdListSchema()
