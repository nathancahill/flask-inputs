## Flask-Inputs

[![Build Status](https://travis-ci.org/nathancahill/flask-inputs.svg)](https://travis-ci.org/nathancahill/flask-inputs)
[![Coverage Status](https://coveralls.io/repos/nathancahill/flask-inputs/badge.svg?branch=master&service=github)](https://coveralls.io/github/nathancahill/flask-inputs?branch=master)


The Flask-Inputs project has three goals:

 - Validate incoming request data
 - Separate inputs and business logic
 - Better error messages

### Installation

To install Flask-Inputs, simply:

```
$ pip install flask-inputs
```

### Usage

Flask-Inputs allows you to define a schema for a request to validate against. It looks like this:

```
from flask_inputs import Imputs
from wtforms.validators import DataRequired

class ApiInputs(Inputs):
    args = {
        'age': [DataRequired()]
    }
    headers = {
        'Authorization': [valid_api_key]
    }
```

A Inputs schema is defined by subclassing `flask_inputs.Inputs`, like WTForms are defined by subclassing `wtforms.form.Form`

Each class variable is a type of input (data you would access through request properties like request.args). These properties are supported:

```
['args', 'form', 'values', 'cookies', 'headers', 'json', 'rule']
```

The variable values are dicts where keys are "fields" and values are that field's validators. To validate the request against the schema, create an instance of the class with the request, and then call `validate()`.

```
@app.route('/my-awesome-api')
def api():
    inputs = ApiInputs(request)

    if not inputs.validate():
        return jsonify(errors=inputs.errors)
```

If `validate()` returns `False`, error messages are listed in `inputs.errors`

Alternatively, to validate an entire input (as opposed to single fields like above), validators can be attached directly:

```
class ApiInputs(Inputs):
    args = [CustomArgValidator()]
```

In this case, the raw input data is passed to the validators.

### JSON Validation

Flask-Inputs provides a validator for JSON data. This requires [jsonschema](https://pypi.python.org/pypi/jsonschema).

```
from flask_inputs.validators import JsonSchema

schema = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'}
    }
}

class JsonInputs(Inputs):
    json = [JsonSchema(schema=schema)]
```


### Goals

#### Validate incoming request data

No matter how complete Flask test coverage is, publicly facing routes are exposed to a number of external inputs that accept semi-arbitrary data, like these:

 - URL rule arguements ([werkzeug.routing.Rule](http://werkzeug.pocoo.org/docs/0.10/routing/#werkzeug.routing.Rule))
 - Form data ([flask.Request.form](http://flask.pocoo.org/docs/0.10/api/#flask.Request.form))
 - Query string ([flask.Request.args](http://flask.pocoo.org/docs/0.10/api/#flask.Request.args))
 - Form data and query string combined ([flask.Request.values](http://flask.pocoo.org/docs/0.10/api/#flask.Request.values))
 - Cookies ([flask.Request.cookies](http://flask.pocoo.org/docs/0.10/api/#flask.Request.cookies))
 - Headers ([flask.Request.headers](http://flask.pocoo.org/docs/0.10/api/#flask.Request.headers))
 - JSON ([flask.Request.json](http://flask.pocoo.org/docs/0.10/api/#flask.Request.json))

Validating this data before using it is tricky. WTForms handles validation for one of these inputs (Form data) really well, wouldn't it be nice to have that for the other inputs?

Flask-Inputs lets you define a WTForms style schema for all incoming request data. Once the request is validated against the schema, request data can be used safely.

#### Separate inputs and business logic

When request data is accessed in a Flask route, it's generally followed by a couple lines for checking data validity.

For example, here is my Cat API:


```python
@app.route('/meow')
def meow():
    cat = request.args.get('cat')
    
    if not cat:
        return jsonify(error='Cat is required')
    
    try:
        cat = int(cat)
    except:
        return jsonify(error='Cat must be a number')
    
    if cat < 0 or cat > 100:
        return jsonify(error='Cat must be between 1 and 100')
    
    # do something with cat
```

This mix of business logic and data validation is verbose, unweildy and hard to test.

Instead, using Flask-Inputs, the data schema can be declared in one place and validated once.

```python
from flask.ext.inputs import Inputs
from wtforms.validators import DataRequired, NumberRange

class CatInputs(Inputs):
    args = {
        'cat': [
            DataRequired('Cat is required'),
            NumberRange(min=1, max=100)
        ]
    }

@app.route('/meow')
def meow():
    inputs = CatInputs(request)

    if not inputs.validate():
        return jsonify(errors=inputs.errors)

    # safely use request.args.get('cat')
```

#### Better error messages

Both APIs and web app users benefit from better error messages. It's easy to do this with Flask-Inputs since the input errors all surface in the same place:

```python
if not inputs.validate():
    if is_api:
        return jsonify(errors=inputs.errors)
     else:
        for msg in inputs.errors:
            flash(msg, 'error)
```
