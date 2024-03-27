from apiflask import Schema, fields
from apiflask.fields import File, String, Integer


class AdmonitionPatchSchema(Schema):
   
    admonishig_user = fields.String()
    admonition_type = fields.String()
    admonition_reason = fields.String()
    processed = fields.Boolean()
    processed_by = fields.String(allow_none = True)
    processed_at = fields.Date(allow_none = True)
    
    class Meta:
        fields = ('admonishing_user','admonition_type', 'admonition_reason', 
                  'processed', 'processed_by', 
                  'processed_at')

admonition_patch_schema = AdmonitionPatchSchema()
admonitions_patch_schema = AdmonitionPatchSchema(many = True)

class AdmonitionInSchema(Schema):
   
    admonished_pupil_id = fields.Integer()
    admonition_type = fields.String()
    admonition_reason = fields.String()
    processed = fields.Boolean()
    processed_by = fields.String(allow_none = True)
    processed_at = fields.Date(allow_none = True)
    file_url = fields.String(allow_none=True)
    admonished_day = fields.Date()
    
    class Meta:
        fields = ('admonished_pupil_id', 'admonished_day', 'admonition_type',
                  'admonition_reason', 'processed', 'processed_by', 
                  'processed_at', 'file_url')

admonition_in_schema = AdmonitionInSchema()
admonitions_in_schema = AdmonitionInSchema(many = True)

class AdmonitionSchema(Schema):
    admonition_id = fields.String()
    admonished_pupil_id = fields.Integer()
    admonition_type = fields.String()
    admonition_reason = fields.String()
    admonishing_user = fields.String()
    processed = fields.Boolean()
    processed_by = fields.String(allow_none = True)
    processed_at = fields.Date(allow_none = True)
    file_url = fields.String(allow_none=True)
    include_fk = True
    admonished_day = fields.Pluck('SchooldaySchema', 'schoolday')
    
    class Meta:
        fields = ('admonition_id', 'admonished_pupil_id', 'admonished_day',
                  'admonition_type', 'admonition_reason', 'admonishing_user',
                  'processed', 'processed_by', 'processed_at', 'file_url')

admonition_schema = AdmonitionSchema()
admonitions_schema = AdmonitionSchema(many = True)

