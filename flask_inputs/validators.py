
import jsonschema
from wtforms.validators import ValidationError


class JsonSchema(object):
    def __init__(self, schema, message=None):
        self.schema = schema
        self.message = message

    def __call__(self, form, field):
        try:
            jsonschema.validate(field.data, self.schema)
        except jsonschema.ValidationError as e:
            raise ValidationError(e.message)
