from typing import List
from flask_restful import Resource

from API.utils import catch_unexpected_exceptions

from .APIResponses import make_response_message, make_response_error, GenericResponseMessages as E_MSG


class Likes(Resource):
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

    @catch_unexpected_exceptions("fetch the Likes collection", True)
    def get(self):
        """The query endpoint of the collection of all likes.

        :return: The list of all liked movies' TMDB ids, ``[]`` by default
        """
        from . import movies_attributes
        non_deleted_keys: List[int] = movies_attributes.filter_valid_non_deleted_keys(movies_attributes.keys())
        liked_movies: List[int] = [movie_id for movie_id in non_deleted_keys if movies_attributes[movie_id].liked]
        return make_response_message(E_MSG.SUCCESS, 200, result=liked_movies)

