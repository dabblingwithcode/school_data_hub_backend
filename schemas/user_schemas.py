from apiflask import Schema, fields
from apiflask.fields import File, String


class NewUserSchema(Schema):
    name = fields.String()
    password = fields.String()
    admin = fields.Boolean()
    role = fields.String()
    credit = fields.Integer()
    class Meta:
        fields = ('name', 'password', 'admin', 'role', 'credit')

new_user_schema = NewUserSchema()
new_users_schema = NewUserSchema(many = True)

class UserSchema(Schema):
    name = fields.String()
    admin = fields.Boolean()
    role = fields.String()
    public_id = fields.String()
    credit = fields.Integer()
    class Meta:
        fields = ('public_id','name', 'role', 'admin','credit')

user_schema = UserSchema()
users_schema = UserSchema(many = True)

class UserLoginSchema(Schema):
    username = fields.String()
    password = fields.String()
    class Meta:
        fields = ('username', 'password')

class UserNewPasswordSchema(Schema):
    old_password = fields.String()
    new_password = fields.String()
    class Meta:
        fields = ('old_password', 'new_password')
