from flask_apispec import MethodResource, marshal_with, doc

from .utils import catch_unexpected_exceptions, require_movie_not_deleted
from .Likes import Likes
from .MovieAttributes import MovieAttributes
from .APIResponses import make_response_message, GenericResponseMessages as E_MSG
from .schemaModels import WebservicesResponseSchema, LikeSchema


class Like(MethodResource):
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

    @doc(description='Get a single Like resource, which represents the "liked" status of a movie.', params={
        'mov_id': {'description': 'The TMDB ID of the chosen movie, for which to fetch the "liked" status'}
    })
    @marshal_with(LikeSchema, code=200)
    @catch_unexpected_exceptions("fetch a Like resource")
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
    
    @doc(description='Set a single Like resource\'s "liked" status to True.', params={
        'mov_id': {'description': 'The TMDB ID of the chosen movie, for which to set the "liked" status'}
    })
    @marshal_with(WebservicesResponseSchema, code=201)
    @catch_unexpected_exceptions("set a Like resource to true")
    @require_movie_not_deleted
    def put(self, mov_id: int):
        """The setter endpoint of a specific like.

        :return: A simple success or error message
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id].liked = True
        else:
            movies_attributes[mov_id] = MovieAttributes(liked=True)

        return make_response_message(E_MSG.SUCCESS, 201)

    @doc(description='Set a single Like resource\'s "liked" status to False.', params={
        'mov_id': {'description': 'The TMDB ID of the chosen movie, for which to set the "liked" status'}
    })
    @marshal_with(WebservicesResponseSchema, code=200)
    @catch_unexpected_exceptions("set a Like resource to false")
    @require_movie_not_deleted
    def delete(self, mov_id: int):
        """The delete endpoint of a specific like. This endpoint sets the resource to false.

        :return: A simple success or error message
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id].liked = False

        return make_response_message(E_MSG.SUCCESS, 200)
