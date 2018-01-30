
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from wtforms.validators import DataRequired, AnyOf


app = Flask(__name__)


class ArgsInputs(Inputs):
    args = {
        'name': [
            DataRequired('Name is required.')
        ],
        'gender': [
            DataRequired('Gender required'),
            AnyOf(values=['male','female'], message='not an accepted one')
        ]
    }

valid_data = 'name=Nathan Cahill&gender=male'
invalid_data = 'name=&gender=both'


class ArgsTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(query_string=valid_data):
            inputs = ArgsInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(query_string=invalid_data):
            inputs = ArgsInputs(request)
            self.assertFalse(inputs.validate())
            print(inputs.errors)

    def test_error_messages(self):
        with app.test_request_context(query_string=invalid_data):
            inputs = ArgsInputs(request)
            inputs.validate()
            self.assertEqual(inputs.errors['name'], 'Name is required.')
