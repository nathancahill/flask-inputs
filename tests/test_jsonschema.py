
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema


app = Flask(__name__)

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'}
    }
}


class JsonInputs(Inputs):
    json = [JsonSchema(schema=schema)]


class JsonInputsMsg(Inputs):
    json = [JsonSchema(schema=schema, message='JSON data did not validate.')]


valid_data = '{"name": "Nathan Cahill"}'
invalid_data = '{"name": 100}'


class JsonSchemaTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(method='POST', data=valid_data, content_type='application/json'):
            inputs = JsonInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
            inputs = JsonInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
            inputs = JsonInputs(request)
            inputs.validate()

            self.assertIn( "100 is not of type 'string'", inputs.errors['_input'])

    def test_custom_error_messages(self):
        with app.test_request_context(method='POST', data=invalid_data, content_type='application/json'):
            inputs = JsonInputsMsg(request)
            inputs.validate()

            self.assertIn('JSON data did not validate.', inputs.errors['_input'])
