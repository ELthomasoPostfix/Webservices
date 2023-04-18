from flask_restful import reqparse
from marshmallow import Schema, fields, validates, ValidationError
from typing import Type


def to_params_type(python_type: Type) -> str:
    """Convert a python type to an apispec params type string.

    The apispec params type string can be passed to the @doc
    decorator to specify a param's type in the generated
    swagger docs.

    Returns a default value, 'unknown type', if the *python_type* is not recognized.
    Valid python types are int, str and bool.

    :param python_type: The python type to convert
    :return: The apispec param type string
    """
    valid_type_mapping = {
        int: "integer",
        str: "string",
        bool: "boolean"
    }
    return valid_type_mapping.get(python_type, "unknown type")

def generate_params_from_parser(parser: reqparse.RequestParser) -> dict:
    """Generate a dict of query parameters that can be passed to the params arg of apispec's doc decorator.

    :param parser: The parser with which the arguments have been registered
    """
    return {
        arg.name: {
            "required": arg.required,
            "in": "query",
            "description": arg.help,
            "type": to_params_type(arg.type)
        } for arg in parser.args
        if 'args' in arg.location
    }

class WebservicesResponseSchema(Schema):
    message = fields.String(required=True, default='default message', metadata={
        'description': 'The response of the API that can be displayed to non-technical users of a consumer application of the API',
    })
    error= fields.String(required=False, metadata={
        'description': 'An optional, technical error message',
    })

class WebservicesResultSchema(WebservicesResponseSchema):
    result = fields.List(fields.Raw, required=True, default=[], metadata={
        'description': 'A generic list of results',
    })

class LikeSchema(WebservicesResponseSchema):
    id = fields.Integer(required=True, metadata={
        'description': 'The TMDB movie id to get the "liked" status of',
    })
    liked = fields.Boolean(required=True, metadata={
        'description': 'The "liked" status of the specified movie',
    })

class LikesSchema(WebservicesResultSchema):
    result = fields.List(fields.Integer, required=True, default=[], metadata={
        'description': 'The list of TMDB movie ids with a "liked" status of True',
    })

movie_field_type = fields.Dict(keys=fields.String, required=True, metadata={
        'description': 'The TMDB primary movie data, with added "liked" status of the movie under the key "liked"',
})

class MovieSchema(WebservicesResponseSchema):
    result = movie_field_type

    @validates('result')
    def validate_result_dict(self, value):
        mandatory_keys = ['liked']  # List of mandatory keys
        missing_keys = set(mandatory_keys) - set(value.keys())
        if missing_keys:
            raise ValidationError(f"Missing mandatory keys: {', '.join(missing_keys)}")

class MoviesSchema(WebservicesResultSchema):
    result = fields.List(movie_field_type, required=True, default=[], metadata={
        'description': 'A list of Movie resources',
    })
