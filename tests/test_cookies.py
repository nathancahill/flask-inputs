
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from werkzeug.datastructures import MultiDict
from wtforms.validators import DataRequired


app = Flask(__name__)


class CookiesInputs(Inputs):
    cookies = {
        'name': [
            DataRequired('Name cookie missing.')
        ]
    }

valid_data = MultiDict([('Cookie', 'name=Nathan Cahill')])
invalid_data = MultiDict([('Cookie', 'name=')])


class CookiesTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(headers=valid_data):
            inputs = CookiesInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(headers=invalid_data):
            inputs = CookiesInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(headers=invalid_data):
            inputs = CookiesInputs(request)
            inputs.validate()

            self.assertEqual(inputs.errors['name'], 'Name cookie missing.')
