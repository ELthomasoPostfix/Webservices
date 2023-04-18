from flask_apispec import MethodResource, marshal_with, doc
from typing import List

from .utils import catch_unexpected_exceptions
from .APIResponses import make_response_message, GenericResponseMessages as E_MSG
from .schemaModels import LikesSchema



class Likes(MethodResource):
    """The api endpoint that represents the collection of all like resources.

    A like is simply a TMDB movie id, linked to a boolean describing whether
    that specific movie has been liked or not.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Likes collection of Like resources.

        :return: The route string
        """
        return "/likes"

    @doc(description="""The simplified collection of all Like resources.
    The "liked" resource is comprised solely of a status boolean, so a list of all movies with a \"liked\" status of True is returned.""")
    @marshal_with(LikesSchema, code=200)
    @catch_unexpected_exceptions("fetch the Likes collection")
    def get(self):
        """The query endpoint of the collection of all likes.

        :return: A LikesSchema instance
        """
        from . import movies_attributes
        non_deleted_keys: List[int] = movies_attributes.prune_deleted_keys(movies_attributes.keys())
        liked_movies: List[int] = [movie_id for movie_id in non_deleted_keys if movies_attributes.is_liked(movie_id)]
        return make_response_message(E_MSG.SUCCESS, 200, result=liked_movies)

