from marshmallow import Schema, fields

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
