
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from wtforms.validators import DataRequired, Email


app = Flask(__name__)


class ValuesInputs(Inputs):
    values = {
        'name': [
            DataRequired('Name is required.')
        ],
        'email': [
            Email('Email must be valid.')
        ]
    }

valid_args = 'name=Nathan Cahill'
invalid_args = 'name='

valid_data = dict(email='nathan@nathancahill.com')
invalid_data = dict(email='nathan')


class ArgsTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(method='POST', query_string=valid_args, data=valid_data):
            inputs = ValuesInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(method='POST', query_string=invalid_args, data=invalid_data):
            inputs = ValuesInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(method='POST', query_string=invalid_args, data=invalid_data):
            inputs = ValuesInputs(request)
            inputs.validate()

            self.assertIn('Name is required.', inputs.errors.values())
            self.assertIn('Email must be valid.', inputs.errors.values())
