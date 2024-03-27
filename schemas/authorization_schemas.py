from apiflask import Schema, fields

##############################
#- PUPIL AUTHORIZATION SCHEMA
##############################

class PupilAuthorizationInSchema(Schema):
    status = fields.Boolean(allow_none=True)
    comment = fields.String(allow_none=True)
    file_url = fields.String(allow_none=True)
    #origin_authorization = fields.String()
    class Meta:
        fields = ('status', 'comment',  
                  'file_url',)

pupil_authorization_in_schema = PupilAuthorizationInSchema()
pupil_authorizations_in_schema = PupilAuthorizationInSchema(many=True)


class PupilAuthorizationSchema(Schema):
    pupil_id = fields.Integer()
    status = fields.Boolean(allow_none=True)
    comment = fields.String(allow_none=True)
    created_by = fields.String()
    file_url = fields.String(allow_none=True)
    origin_authorization = fields.String()
    class Meta:
        fields = ('pupil_id', 'status', 'comment', 'created_by', 
                  'file_url', 'origin_authorization')

pupil_authorization_schema = PupilAuthorizationSchema()
pupil_authorizations_schema = PupilAuthorizationSchema(many=True)

########################
#- AUTHORIZATION SCHEMA
########################

class AuthorizationInGroupSchema(Schema):
    authorization_name = fields.String()
    authorization_description = fields.String()
    pupils = fields.List(fields.Integer())  
    class Meta:
        fields = ('authorization_name', 'authorization_description', 'pupils')

authorization_in_group_schema = AuthorizationInGroupSchema()
authorizations_in_group_schema = AuthorizationInGroupSchema(many= True)

class AuthorizationInSchema(Schema):
    authorization_name = fields.String()
    authorization_description = fields.String()  
    class Meta:
        fields = ('authorization_name', 'authorization_description')

authorization_in_schema = AuthorizationInSchema()
authorizations_in_schema = AuthorizationInSchema(many= True)

class AuthorizationSchema(Schema):
    authorization_id = fields.String()
    authorization_name = fields.String()
    authorization_description = fields.String()
    created_by = fields.String()
    authorized_pupils = fields.List(fields.Nested(PupilAuthorizationSchema))    
    class Meta:
        fields = ('authorization_id', 'authorization_name', 'authorization_description', 'created_by', 'authorized_pupils')

authorization_schema = AuthorizationSchema()
authorizations_schema = AuthorizationSchema(many= True)

########################
#- AUTHORIZATION FLAT SCHEMA
########################

class AuthorizationFlatSchema(Schema):
    authorization_id = fields.String()
    authorization_name = fields.String()
    authorization_description = fields.String()
    created_by = fields.String()    
    class Meta:
        fields = ('authorization_id', 'authorization_name', 'authorization_description', 'created_by')

authorization_flat_schema = AuthorizationFlatSchema()
authorizations_flat_schema = AuthorizationFlatSchema(many= True)
