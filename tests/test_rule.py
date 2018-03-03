
import unittest

from flask import Flask, request
from flask_inputs import Inputs
from wtforms.validators import AnyOf


app = Flask(__name__)
app.add_url_rule('/<color>', 'color')


class RuleInputs(Inputs):
    rule = {
        'color': [
            AnyOf(['red', 'green', 'blue'], message='Not a valid color.')
        ]
    }

valid_data = '/green'
invalid_data = '/yellow'


class RuleTest(unittest.TestCase):
    def test_valid(self):
        with app.test_request_context(valid_data):
            inputs = RuleInputs(request)

            self.assertTrue(inputs.validate())

    def test_invalid(self):
        with app.test_request_context(invalid_data):
            inputs = RuleInputs(request)

            self.assertFalse(inputs.validate())

    def test_error_messages(self):
        with app.test_request_context(invalid_data):
            inputs = RuleInputs(request)
            inputs.validate()

            self.assertIn('Not a valid color.', inputs.errors['color'])
