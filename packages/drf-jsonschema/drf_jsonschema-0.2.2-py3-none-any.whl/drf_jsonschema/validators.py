from django.utils.deconstruct import deconstructible
from jsonschema.validators import Draft202012Validator

from .exceptions import SchemaValidationError


# Validate if json comply with JSONSchema
@deconstructible
class JsonSchemaFieldValidator():

    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        validator = Draft202012Validator(self.schema)
        # Pass `bool` as key function to preserve original order
        error_iterator = sorted(validator.iter_errors(value), key=bool)
        # error_iterator will be empty if no error is found
        if not error_iterator:
            return
        error_list = self.convert_error_list(error_iterator)
        # get nested dictionary of errors message
        raise SchemaValidationError(error_list, error_iterator=error_iterator)

    def convert_error_list(self, error_list):
        # loop through error_list and store jsonschema properties name
        # with json error message as key-value pairs
        result = []
        for error in error_list:
            result.append(f'{error.json_path}: {error.message}')
        return result
