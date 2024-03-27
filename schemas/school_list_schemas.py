from apiflask import Schema, fields

####################
#- PUPIL LIST SCHEMA
####################

class PupilListPatchSchema(Schema):
    pupil_list_status = fields.Boolean(allow_none=True)
    pupil_list_comment = fields.String(allow_none=True)
    class Meta:
        fields = ('listed_pupil_id','pupil_list_status', 'pupil_list_comment',
                  'pupil_list_entry_by')
pupil_list_patch_schema = PupilListPatchSchema()
pupil_lists_patch_schema = PupilListPatchSchema(many=True)

class PupilListSchema(Schema):
    listed_pupil_id = fields.Integer()
    pupil_list_status = fields.Boolean(allow_none=True)
    pupil_list_comment = fields.String(allow_none=True)
    pupil_list_entry_by = fields.String()
    class Meta:
        fields = ('listed_pupil_id','pupil_list_status', 'pupil_list_comment',
                  'pupil_list_entry_by')
pupil_list_schema = PupilListSchema()
pupil_lists_schema = PupilListSchema(many=True)

class PupilProfileListSchema(Schema):
    origin_list = fields.String()
    pupil_list_status = fields.Boolean(allow_none=True)
    pupil_list_comment = fields.String(allow_none=True)
    pupil_list_entry_by = fields.String() 
    class Meta:
        fields = ('origin_list', 'pupil_list_status', 'pupil_list_comment',
                  'pupil_list_entry_by')
pupilprofilelist_schema = PupilListSchema()
pupilprofilelists_schema = PupilListSchema(many=True)

#####################
#- SCHOOL LIST SCHEMA
#####################

class SchoolListInGroupSchema(Schema):
    list_name = fields.String()
    list_description = fields.String()
    visibility = fields.String()
    pupils = fields.List(fields.Integer())  
    class Meta:
        fields = ('list_name', 'list_description',
                  'visibility', 'pupils')
school_list_in_group_schema = SchoolListInGroupSchema()
school_lists_in_group_schema = SchoolListInGroupSchema(many= True)

class SchoolListInSchema(Schema):
    list_name = fields.String()
    list_description = fields.String()
    visibility = fields.String()  
    class Meta:
        fields = ('list_name', 'list_description',
                  'visibility')
school_list_in_schema = SchoolListInSchema()
school_lists_in_schema = SchoolListInSchema(many= True)

class SchoolListSchema(Schema):
    list_id = fields.String()
    list_name = fields.String()
    list_description = fields.String()
    created_by = fields.String()
    visibility = fields.String()
    pupils_in_list = fields.List(fields.Nested(PupilListSchema))   
    class Meta:
        fields = ('list_id', 'list_name', 'list_description',
                  'created_by', 'visibility', 'pupils_in_list')
school_list_schema = SchoolListSchema()
school_lists_schema = SchoolListSchema(many= True)

class SchoolListFlatSchema(Schema):
    list_id = fields.String()
    list_name = fields.String()
    list_description = fields.String()
    created_by = fields.String()
    visibility = fields.String()    
    class Meta:
        fields = ('list_id', 'list_name', 'list_description',
                  'created_by', 'visibility')
school_list_flat_schema = SchoolListFlatSchema()
school_lists_flat_schema = SchoolListFlatSchema(many= True)
