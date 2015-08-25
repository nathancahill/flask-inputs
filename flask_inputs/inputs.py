
import collections
from itertools import chain

from werkzeug.datastructures import MultiDict

from wtforms.form import BaseForm
from wtforms.fields import Field


class Inputs(object):
    _valid_attributes = ['args', 'form', 'values', 'cookies',
                         'headers', 'json', 'rule']

    def __init__(self, request):
        """
        :param request: The Flask request object to use for validation.

        To define request inputs, one makes a subclass of Inputs and defines
        each of the incoming request data attributes as class attributes:

        class TellInputs(Inputs):
            rule = {'name': [Length(min=3, max=10)]}
            args = {'message': [DataRequired()]}

        Internally, each request attribute is a form, and each request
        attribute key is a field. The validators are attached to their fields.
        """
        self.errors = []
        self._request = request
        self._forms = dict()

        for name in dir(self):
            if not name.startswith('_') and name not in ['errors', 'validate']:
                input = getattr(self, name)
                fields = dict()

                if isinstance(input, dict):
                    for field, validators in input.iteritems():
                        fields[field] = Field(validators=validators)
                elif isinstance(input, collections.Iterable):
                    fields['_input'] = Field(validators=input)

                self._forms[name] = BaseForm(fields)

    def _get_values(self, attribute, coerse=True):
        """
        :param attribute: Request attribute to return values for.

        Returns a MultiDict for compatibility with wtforms form data.
        """
        if attribute in self._valid_attributes:
            if attribute == 'rule':
                ret = self._request.view_args
            else:
                ret = getattr(self._request, attribute)

            if coerse:
                return MultiDict(ret)
            else:
                return MultiDict(dict(_input=ret))

    def validate(self):
        """
        Validate incoming request data. Returns True if all data is valid.
        """
        success = True

        for attribute, form in self._forms.iteritems():
            if '_input' in form._fields:
                form.process(self._get_values(attribute, coerse=False))
            else:
                form.process(self._get_values(attribute))

            if not form.validate():
                success = False
                self.errors += chain(*form.errors.values())

        return success
