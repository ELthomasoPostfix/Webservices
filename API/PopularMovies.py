import requests
from requests.exceptions import JSONDecodeError
from flask_restful import Resource, reqparse, current_app

from .utils import catch_unexpected_exceptions
from .exceptions import NotOKTMDB
from .APIResponses import make_response_message, make_response_error, GenericResponseMessages as E_MSG, TMDBResponseMessages as E_TMDB
from .APIClients import TMDBClient
from .Movies import Movies


class MoviesParameters(object):
    """An enum of the parameters used by the PopularMovies resource.

    For descriptions of the parameters, refer to the help argument
    specified in their addition as arguments to the reqparser below.
    """
    amount: str = "amount"

"""The query arguments passed to this endpoint facilitate
features related to retrieving the list of the first X
popular movies.

The query parameters correspond to the required project features
in the following way:
    * MoviesParameters.amount: 1.

The feature numbers (i.e. 'x.') refer to the features in the
same order as they are listed in the Project Specification
section of the README.
"""
parser = reqparse.RequestParser()
parser.add_argument(MoviesParameters.amount, type=int, required=True, location=('args',),
                    help="The amount of popular movies, as a positive integer")


class PopularMovies(Resource):
    """The api endpoint that represents the collection of all popular Movie resources.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the PopularMovies collection of popular Movie resources.

        :return: The route string
        """
        return f"{Movies.route()}/popular"

    @catch_unexpected_exceptions("query the Movies collection")
    def get(self):
        """The query endpoint of the collection of all popular Movie resources.

        :return: The first x popular movies if successful, else an error response
        """
        args = parser.parse_args()
        try:
            from . import movies_attributes
            popular_x: int = args[MoviesParameters.amount]

            if popular_x < 0:
                return make_response_error(E_MSG.MALFORMED_REQ,
                                            f"The {MoviesParameters.amount} parameter must be positive",
                                            400)

            # Setup
            popular_x_movies = []
            remaining_movies: int = popular_x
            total_pages_available: int = 1
            current_page: int = 1

            # The TMDB popular API responds with a single fixed size page at a time
            while remaining_movies > 0 and current_page <= total_pages_available:
                # Query TMDB API
                tmdb_resp = TMDBClient.get_popular_page(page=current_page)

                if not tmdb_resp.ok:
                    raise NotOKTMDB()

                tmdb_resp_json = tmdb_resp.json()
                results = tmdb_resp_json["results"]
                results = [
                    result
                    for result in results
                    if not movies_attributes.is_deleted(result["id"])
                ]
                results = results[:remaining_movies]
                for movie in results:
                    movie_id: int = movie["id"]
                    movie["liked"] = movies_attributes.is_liked(movie_id)
                total_pages_available = tmdb_resp_json["total_pages"]

                # Bookkeeping
                remaining_movies -= len(results)
                current_page += 1

                # Aggregate results
                popular_x_movies.extend(results)

            return make_response_message(E_MSG.SUCCESS, 200, result=popular_x_movies)
        except JSONDecodeError as e:
            return make_response_error(E_MSG.ERROR, E_TMDB.ERROR_JSON_DECODE, 502)
        except NotOKTMDB as e:
            return make_response_error(E_MSG.ERROR, E_TMDB.NOT_OK, 502)


