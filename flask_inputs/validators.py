
import jsonschema
from wtforms.validators import ValidationError


class JsonSchema(object):
    def __init__(self, schema, message=None):
        """Helper class for JSON validation using jsonschema.

        :param schema: JSON schema to validate against.
        :param message: Error message to return. Defaults to jsonschema's errors.

        :raises: wtforms.validators.ValidationError
        """
        self.schema = schema
        self.message = message

    def __call__(self, form, field):
        try:
            jsonschema.validate(field.data, self.schema)
        except jsonschema.ValidationError as e:
            if self.message:
                raise ValidationError(self.message)

            raise ValidationError(e.message)
