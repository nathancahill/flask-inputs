
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from wtforms.validators import DataRequired


app = Flask(__name__)


class ArgsInputs(Inputs):
    args = {
        'name': [
            DataRequired('Name is required.')
        ]
    }

valid_data = 'name=Nathan Cahill'
invalid_data = 'name='


class ArgsTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(query_string=valid_data):
            inputs = ArgsInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(query_string=invalid_data):
            inputs = ArgsInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(query_string=invalid_data):
            inputs = ArgsInputs(request)
            inputs.validate()

            self.assertEqual(inputs.errors, ['Name is required.'])
