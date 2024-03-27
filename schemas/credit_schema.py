from apiflask import Schema, fields

#- CREDIT HISTORY LOG SCHEMA
############################

class CreditHistoryLogSchema(Schema):
    credit = fields.Integer()
    operation = fields.Integer()
    created_by = fields.String()
    created_at = fields.Date()
    class Meta:
        fields = ('operation', 'created_by', 'created_at', 'credit')

credit_history_log_schema = CreditHistoryLogSchema()
credit_history_logs_schema = CreditHistoryLogSchema(many = True)
