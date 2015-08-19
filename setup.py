
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name='Flask-Inputs',
    version='0.0.1',
    description='Incoming request data validation',
    long_description=long_description,
    url='https://github.com/nathancahill/flask-inputs',
    author='Nathan Cahill',
    author_email='nathan@nathancahill.com',
    license='MIT',
    keywords='flask validation wtforms',
    py_modules=['flask_inputs'],
    install_requires=['flask', 'wtforms'],
)
