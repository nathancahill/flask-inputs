
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from werkzeug.datastructures import MultiDict
from wtforms.validators import AnyOf


app = Flask(__name__)


class HeadersInputs(Inputs):
    headers = {
        'Authorization': [
            AnyOf(['9787B9FF6DDCB'], message='Invalid API key.')
        ]
    }

valid_data = MultiDict([('Authorization', '9787B9FF6DDCB')])
invalid_data = MultiDict([('Authorization', 'wrongkey')])


class HeadersTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(headers=valid_data):
            inputs = HeadersInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(headers=invalid_data):
            inputs = HeadersInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(headers=invalid_data):
            inputs = HeadersInputs(request)
            inputs.validate()

            self.assertIn('Invalid API key.', inputs.errors['Authorization'])
