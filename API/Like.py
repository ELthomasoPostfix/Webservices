from flask_restful import Resource

from API.MovieAttributes import MovieAttributes

from .utils import catch_unexpected_exceptions, require_movie_not_deleted
from .Likes import Likes
from .APIResponses import make_response_message, make_response_error, GenericResponseMessages as E_MSG


class Like(Resource):
    """The api endpoint that represents a single like resource.

    A like is simply a TMDB movie id, linked to a boolean describing whether
    that specific movie has been liked or not.

    This resource supports project requirement 7.: liking/un-liking movies.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Like resource.

        :return: The route string
        """
        return f"{Likes.route()}/<int:mov_id>"

    @catch_unexpected_exceptions("fetch a Like resource", True)
    @require_movie_not_deleted
    def get(self, mov_id: int):
        """The query endpoint of a specific like.

        :return: The like state of the specified TMDB movie
        """
        from . import movies_attributes
        liked: bool = False

        if mov_id in movies_attributes:
            liked = movies_attributes[mov_id].liked

        return make_response_message(E_MSG.SUCCESS, 200, id=mov_id, liked=liked)
    
    @catch_unexpected_exceptions("set a Like resource to true")
    @require_movie_not_deleted
    def put(self, mov_id: int):
        """The setter endpoint of a specific like.

        :return: None
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id].liked = True
        else:
            movies_attributes[mov_id] = MovieAttributes(liked=True)

        return make_response_message(E_MSG.SUCCESS, 201)

    @catch_unexpected_exceptions("set a Like resource to false")
    @require_movie_not_deleted
    def delete(self, mov_id: int):
        """The delete endpoint of a specific like. This endpoint sets the resource to false.

        :return: None
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id].liked = False

        return make_response_message(E_MSG.SUCCESS, 200)
