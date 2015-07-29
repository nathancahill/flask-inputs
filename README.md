## Flask-Inputs

The Flask-Inputs project has three goals:

 - Incoming request data validation
 - Seperate inputs and business logic
 - Error message responses

### Incoming request data validation

No matter how complete Flask test coverage is, publicly facing routes are exposed to a number of external inputs that accept semi-arbitrary data, like these:

 - URL rule arguements ([werkzeug.routing.Rule](http://werkzeug.pocoo.org/docs/0.10/routing/#werkzeug.routing.Rule))
 - Form data ([flask.Request.form](http://flask.pocoo.org/docs/0.10/api/#flask.Request.form))
 - Query string ([flask.Request.args](http://flask.pocoo.org/docs/0.10/api/#flask.Request.args))
 - Form data and query string combined ([flask.Request.values](http://flask.pocoo.org/docs/0.10/api/#flask.Request.values))
 - Cookies ([flask.Request.cookies](http://flask.pocoo.org/docs/0.10/api/#flask.Request.cookies))
 - Headers ([flask.Request.headers](http://flask.pocoo.org/docs/0.10/api/#flask.Request.headers))

Validating this data before using it is tricky. WTForms handles validation for one of these inputs (Form data) really well, wouldn't it be nice to have that for the other inputs?

Flask-Inputs lets you define a WTForms style schema for all incoming request data. Once the request is validated against the schema, request data can be used safely.

### Seperate inputs and business logic
 
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
    
    // do something with cat
```

This mix of business logic and data validation is verbose, unweildy and hard to test.

Instead, using Flask-Inputs, the data schema can be declared in one place and validated once.

```python
from flask.ext.inputs import Inputs

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

    // safely use request.args.get('cat')
```

### Error message responses

Both APIs and web app users benefit from better error responses. It's easy to do this with Flask-Inputs:

```python
if not inputs.validate():
    if is_api:
        return jsonify(errors=inputs.errors)
     else:
        for msg in inputs.errors:
            flash(msg, 'error)
```
