from json import JSONDecodeError
import requests
from flask_restful import Resource, current_app

from .utils import catch_unexpected_exceptions, require_movie_not_deleted
from .exceptions import NotOKTMDB
from .MovieAttributes import MovieAttributes
from .Movies import Movies
from .APIResponses import GenericResponseMessages as E_MSG, TMDBResponseMessages as E_TMDB, make_response_error, make_response_message


class Movie(Resource):
    """The api endpoint that represents a single movie resource.

    This resource supports project requirement 6.: ’delete’ movies
    by implementing the delete http method.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Movie resource.

        :return: The route string
        """
        return f"{Movies.route()}/<int:mov_id>"

    @staticmethod
    def get_movie(movie_id: int) -> requests.Response:
        """Get the primary information about a movie from the TMDB ``/movie/{movie_id}`` API.

        :param movie_id: Which movie's information to retrieve
        :return: The TMDB response, containing the requested movie if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={current_app.config['API_KEY_TMDB']}")

    @catch_unexpected_exceptions("fetch a movie's primary information")
    @require_movie_not_deleted
    def get(self, mov_id: int):
        """The query endpoint of the primary information for a single, specific movie resource.

        :return: The movie's primary information
        """
        try:
            from . import movies_attributes
            # Query TMDB API
            # Has Protection against change in pagecount during long query (large popularx)
            tmdb_resp = self.get_movie(movie_id=mov_id)
            if tmdb_resp.status_code == 404:
                return make_response_error(E_MSG.ERROR, f"The movie resource, {mov_id}, does not exist", 404)
            if not tmdb_resp.ok:
                raise NotOKTMDB()

            tmdb_resp_json=tmdb_resp.json()
            tmdb_resp_json["liked"] = movies_attributes.is_liked(mov_id)
            return make_response_message(E_MSG.SUCCESS, 200, result=tmdb_resp_json)
        except JSONDecodeError as e:
            return make_response_error(E_MSG.ERROR, "TMDB gave an invalid response", 502)
        except NotOKTMDB as e:
            return make_response_error(E_MSG.ERROR, E_TMDB.NOT_OK, 502)

    @catch_unexpected_exceptions("delete a movie")
    @require_movie_not_deleted
    def delete(self, mov_id: int):
        """The delete endpoint for a single, specific movie resource.

        All deleted movies are excluded from being returned by any of
        the related API endpoints.

        :return: None
        """
        from . import movies_attributes

        if mov_id in movies_attributes:
            movies_attributes[mov_id].deleted = True
        else:
            movies_attributes[mov_id] = MovieAttributes(deleted=True)

        return make_response_message(E_MSG.SUCCESS, 200)
