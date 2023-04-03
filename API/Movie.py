from json import JSONDecodeError
import requests
from flask_restful import Resource, current_app

from .utils import catch_unexpected_exceptions
from .MovieAttributes import MovieAttributes
from .Movies import Movies
from .APIResponses import GenericResponseMessages as E_MSG, make_response_error, make_response_message


class Movie(Resource):
    """The api endpoint that represents a single movie resource.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Movie resource.

        :return: The route string
        """
        return f"{Movies.route()}/<int:mov_id>"

    @staticmethod
    def getMovie(movie_id: int) -> requests.Response:
        """Get the primary information about a movie from the TMDB ``/movie/{movie_id}`` API.

        :param movie_id: Which movie's information to retrieve
        :return: The movie's primary information in json format if successful, else ``{}``
        """
        return requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={current_app.config['API_KEY_TMDB']}")

    @catch_unexpected_exceptions("fetch a movie's primary information")
    def get(self, mov_id: int):
        """The query endpoint of the primary information for a single, specific movie resource.

        :return: The movie's 'deleted' status and, if not deleted, its primary information
        """
        from . import movies_attributes

        # Do not return deleted movies
        is_deleted: bool = movies_attributes.get(mov_id, MovieAttributes(deleted=False)).deleted
        if is_deleted:
            return make_response_message(E_MSG.SUCCESS, 204)

        # Query TMDB API
        # Has Protection against change in pagecount during long query (large popularx)
        tmdb_resp = self.getMovie(movie_id=mov_id)
        if not tmdb_resp.ok:
            return make_response_error(E_MSG.ERROR, "TMDB raised an exception while fetching a movie's primary information", 500)

        try:
            return make_response_message(E_MSG.SUCCESS, 200, result=tmdb_resp.json(), deleted=is_deleted)
        except JSONDecodeError as e:
            return make_response_error(E_MSG.ERROR, "TMDB gave an invalid response", 502)

    @catch_unexpected_exceptions("deleting a movie")
    def delete(self, mov_id: int):
        """The delete endpoint for a single, specific movie resource.

        All deleted movies are excluded from being returned by any of
        the related API endpoints.

        :return: None
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id] = MovieAttributes(deleted=True)
        else:
            movies_attributes[mov_id].deleted = True

        return make_response_message(E_MSG.SUCCESS, 200)
