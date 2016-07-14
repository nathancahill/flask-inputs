.. Flask-Inputs documentation master file, created by
   sphinx-quickstart on Tue Aug 25 16:12:54 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Flask-Inputs
============

WTForms is awesome for validating POST data. What about other request data?

The **Flask-Inputs** extension adds support for WTForms to validate request
data from args to headers to json.

Installing Flask-Inputs
-----------------------

Install with **pip**::

    pip install flask-inputs

Or download the latest version from Github::

    git clone https://github.com/nathancahill/flask-inputs.git
    cd flask-inputs
    python setup.py install

Example Usage
-------------

Let's say we have an API for customer data. Our route looks like this::

    @api.route('/customer/<int:id>')
    def customer(id):
        pass

Input validators are organized in a class, by type (args, headers, etc). We
give each input field a list of validators. Let's start by validating the URL
rule::

    from flask_inputs import Inputs
    from wtforms.validators import DataRequired

    class CustomerInputs(Inputs):
        rule = {
            'id': [DataRequired()]
        }

Like WTForms, built-in validators and custom validators are supported::

    def customer_exists(form, field):
        if not Customer.query.get(field.data):
            raise ValidationError('Customer does not exist.')

    class CustomerInputs(Inputs):
        rule = {
            'id': [DataRequired(), customer_exists]
        }

To validate the inputs, instantiate the Inputs class with the request object::

    @api.route('/customer/<int:id>')
    def customer(id):
        inputs = CustomerInputs(request)

        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

Adding more validators is easy now, like adding validation for API keys passed
in the Authorization header::

    class CustomerInputs(Inputs):
        rule = {
            'id': [DataRequired(), customer_exists]
        }
        headers = {
            'Authorization': [DataRequired(), valid_api_key]
        }

Advanced Usage
--------------

Inputs can be validated at any point in the request lifecycle. It can be
helpful to put validation in a @before_request function, either in
with an app or blueprint object::

    from flask import Blueprint

    api = Blueprint('api', __name__)

    @api.before_request
    def before():
        inputs = ApiInputs(request)

        if not inputs.validate():
            return jsonify(success=False, errors=inputs.errors)

Input objects also work with mixins, like WTForms. Common validators can be
shared like this::

    class ApiKeyValidation():
        headers = {
            'Authorization': [DataRequired(), valid_api_key]
        }

    class CustomerInputs(Inputs, ApiKeyValidation):
        pass

    class ProductInputs(Inputs, ApiKeyValidation):
        pass

This makes changing requirements in future simple. For example, if API keys
are switched from the Authorization header to a key arg, it's only needs to be
changed in one place.

JSON Validation
---------------

Flask-Inputs supports JSON schema validation with
`jsonschema <https://pypi.python.org/pypi/jsonschema>`_. JSON data posted
in a request can be validated like this::

    from flask_inputs.validators import JsonSchema

    schema = {
        'type': 'object',
        'properties': {
            'name': {'type': 'string'}
        }
    }

    class JsonInputs(Inputs):
        json = [JsonSchema(schema=schema)]

API
---

.. module:: flask_inputs

.. autoclass:: Inputs
    :members: validate, errors, valid_attrs

.. module:: flask_inputs.validators

.. autoclass:: JsonSchema
