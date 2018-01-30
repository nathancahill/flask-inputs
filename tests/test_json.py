
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from wtforms.validators import DataRequired


app = Flask(__name__)


class JsonInputs(Inputs):
    json = {
        'name': [
            DataRequired('Name is required.')
        ]
    }

valid_data = '{"name": "Nathan Cahill"}'
invalid_data = '{"name": ""}'


class JsonTest(unittest.TestCase):
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

            self.assertEqual(inputs.errors['name'], 'Name is required.')
