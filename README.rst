Flask-Inputs
============

   ⚠️ This package is no longer maintained. The Flask-Inputs package on
   PyPi (version 0.3.0) supports up to Python 3.8. Any further breaking
   changes will no longer be supported or fixed. Feel free to fork this
   project and continue improving it.

|Project Status| |License| |Build Status| |Coverage Status|

Introduction
------------

WTForms is awesome for validating POST data. What about other request
data?

The **Flask-Inputs** extension adds support for WTForms to validate
request data from args to headers to json.

Installation
------------

To install Flask-Inputs, simply:

::

   $ pip install flask-inputs

JSON validation requires
`jsonschema <https://pypi.python.org/pypi/jsonschema>`__:

::

   $ pip install jsonschema

Documentation
-------------

Documentation is available at http://pythonhosted.org/Flask-Inputs

Contribute
----------

Feel free to fork this repository and republish it. I will no longer be
maintaining this project.

License
-------

`MIT <./LICENSE.md>`__

.. |Project Status| image:: https://img.shields.io/badge/status-abandoned-red
.. |License| image:: https://img.shields.io/badge/license-MIT-green
   :target: ./LICENSE.md
.. |Build Status| image:: https://travis-ci.org/nathancahill/flask-inputs.svg
   :target: https://travis-ci.org/nathancahill/flask-inputs
.. |Coverage Status| image:: https://coveralls.io/repos/nathancahill/flask-inputs/badge.svg?branch=master&service=github
   :target: https://coveralls.io/github/nathancahill/flask-inputs?branch=master
