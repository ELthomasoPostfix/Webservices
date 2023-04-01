import requests
from requests.exceptions import JSONDecodeError, InvalidJSONError
from flask_restful import Resource, reqparse, current_app

from .APIResponses import make_response_message, make_response_error, GenericResponseMessages as E_MSG


class MoviesParameters(object):
    """An enum of the parameters used by the Movies resource
    to provide filtering features.

    For descriptions of the parameters, refer to the help argument
    specified in their addition as arguments to the reqparser below.
    """
    popular: str = "popularx"

"""The query arguments passed to this endpoint facilitate
features related to retrieving the list of available movies.
Thus, this endpoint provides filtering functions on the
collection of all movies.

The query parameters correspond to the required project features
in the following way:
    * popular: 1.

The feature numbers (i.e. 'x.') refer to the features in the
same order as they are listed in the Project Specification
section of the README
"""
parser = reqparse.RequestParser()
parser.add_argument(MoviesParameters.popular, type=int, required=False, location=('args',),
                    help="Return the first x popular movies")


class Movies(Resource):
    """The api endpoint that represents the collection of all movie resources.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Movies collection of Movie resources.

        :return: The route string
        """
        return "/movies"

    @staticmethod
    def getPopularPage(page: int) -> requests.Response:
        """Get a *page* of popular movies from the TMDB ``/movie/popular`` API.
        
        :param page: Which page to retrieve
        :return: The page in json format if successful, else ``{}``
        """
        # guard clause, based on TMDB page param requirements
        if page < 1 or page > 1000:
            return {}
        return requests.get(f"https://api.themoviedb.org/3/movie/popular?page={page}&api_key={current_app.config['API_KEY_TMDB']}")

    def get(self):
        """The filter/search endpoint of the collection of all movies.

        The filtering system works on the principle of a whitelist. The
        base response is the empty dict, ``{}``. A base set of movies
        needs to be selected, e.g. the x most popular movies. Adding
        filters via the query string allows narrowing donw the results.

        :return: The result of the filter query, ``{}`` by default
        """
        args = parser.parse_args()

        try:
            popular_x: int | None = args[MoviesParameters.popular]
            result: dict = dict()

            if popular_x is not None:
                if popular_x < 0:
                    return make_response_error(E_MSG.MALFORMED_REQ,
                                               f"The {MoviesParameters.popular} parameter must be positive",
                                               400)

                popular_x_movies = []
                remaining_movies: int = popular_x
                total_pages_available: int = 1
                current_page: int = 1

                while remaining_movies > 0 and current_page <= total_pages_available:
                    # Query TMDB API
                    # Has Protection against change in pagecount during long query (large popularx)
                    tmdb_resp = self.getPopularPage(page=current_page)

                    if not tmdb_resp.ok:
                        return make_response_error(E_MSG.ERROR, "TMDB raised an exception while fetching a popular page", 500)


                    tmdb_resp_json = tmdb_resp.json()
                    total_pages_available = tmdb_resp_json["total_pages"]
                    results = tmdb_resp_json["results"][:remaining_movies]

                    # Bookkeeping
                    remaining_movies -= len(results)
                    current_page += 1

                    # Append results
                    popular_x_movies.extend(results)

                result[MoviesParameters.popular] = popular_x_movies
        except JSONDecodeError as e:
            return make_response_error(E_MSG.ERROR, "TMDB gave an invalid response", 502)
        except Exception as e:
            return make_response_error(E_MSG.UNEXPECTED, "Unexpected exception while querying the Movies collection", 500)

        return make_response_message(E_MSG.SUCCESS, 200, result=result)
