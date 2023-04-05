import collections
import requests
from json import JSONDecodeError
from typing import List, Callable, Set
from flask_restful import Resource, reqparse, current_app
import werkzeug

from .utils import catch_unexpected_exceptions, require_movie_not_deleted
from .exceptions import NotOKError
from .Movie import Movie
from .APIResponses import GenericResponseMessages as E_MSG, make_response_error, make_response_message


class SimilarityParameters(object):
    """A class to handle query paramters for the Webservices similarity API.
    
    This class provides both constants that denote the keywords the Webservices
    API accepts as query parameters, as well as static methods that construct the
    corresponding query substrings to pass to the TMDB discover movie API.

    Calling the query substring constructors may cause redundant API calls to
    TMDB, as each of these constructors is fully contained to make for a
    cleaner and shorter implementation. For example, if a constructor method
    needs the movie's primary info it will always query TMDB's `/movie/{movie_id}`
    itself and does not share these results through its return value.
    """

    ACTORS = "overlapping_actors"
    GENRES = "matching_genres"
    RUNTIME = "similar_runtime"

    @staticmethod
    def accepted_parameters():
        """The list of parameters that the Webservices similarity API actively supports"""
        return list(SimilarityParameters.function_mapping().keys())
    
    @staticmethod
    def function_mapping() -> dict[str, Callable[[int], str]]:
        """The mapping from Webservices similarity API query parameters to TMDB discover API query parameters"""
        return {
            SimilarityParameters.ACTORS: SimilarityParameters.get_tmdb_actors_query_substr,
            SimilarityParameters.GENRES: SimilarityParameters.get_tmdb_genres_query_substr,
            SimilarityParameters.RUNTIME: SimilarityParameters.get_tmdb_runtime_query_substr
        }

    @staticmethod
    def get_tmdb_actors_query_substr(movie_id: int) -> str:
        """Get the TMDB discovery api query substring for overlapping cast (actors).

        May raise a `KeyError` or a `JSONDecodeError` in case of an erroneous response
        from TMDB. May raise a `NotOKError` if the TMDB response has an invalid
        status code.
        
        :param movie_id: The movie to select the actors from
        :return: The query substring
        """
        tmdb_resp = Similar.get_credits(movie_id)
        if not tmdb_resp.ok:
            raise NotOKError("TMDB raised an exception while fetching a movie's credits")
        tmdb_resp_json = tmdb_resp.json()
        cast = tmdb_resp_json["cast"]
        actor_ids: List[int] = [person["id"] for person in cast]

        first_two_actors = [str(id) for id in actor_ids[:2]]
        return f"with_cast={','.join(first_two_actors)}"
    
    @staticmethod
    def get_tmdb_genres_query_substr(movie_id: int) -> str:
        """Get the TMDB discovery api query substring for matching genres.

        May raise a `KeyError` or a `JSONDecodeError` in case of an erroneous response
        from TMDB. May raise a `NotOKError` if the TMDB response has an invalid
        status code.

        :param movie_id: The movie to select the genres from
        :return: The query substring
        """
        # Get wanted movie genres
        tmdb_resp = Movie.get_movie(movie_id)
        if not tmdb_resp.ok:
            NotOKError("TMDB raised an exception while fetching a movie's primary information")
        tmdb_resp_json = tmdb_resp.json()
        wanted_genre_ids: List[int] = [genre["id"] for genre in tmdb_resp_json["genres"]]
        wanted_genre_ids = [str(id) for id in wanted_genre_ids]

        # Get unwanted movie genres
        tmdb_resp = Similar.get_movie_genres()
        if not tmdb_resp.ok:
            NotOKError("TMDB raised an exception while fetching all movie genres")
        tmdb_resp_json = tmdb_resp.json()
        unwanted_genre_ids: Set[int] = set([genre["id"] for genre in tmdb_resp_json["genres"]])
        unwanted_genre_ids = set([str(id) for id in unwanted_genre_ids])
        unwanted_genre_ids.difference_update(wanted_genre_ids)

        return f"with_genres={','.join(wanted_genre_ids)}&without_genres={','.join(unwanted_genre_ids)}"
    
    @staticmethod
    def get_tmdb_runtime_query_substr(movie_id: int) -> str:
        """Get the TMDB discovery api query substring for similar runtime.

        May raise a `KeyError` or a `JSONDecodeError` in case of an erroneous response
        from TMDB. May raise a `NotOKError` if the TMDB response has an invalid
        status code.

        :param movie_id: The movie to select the runtime from
        :return: The query substring
        """
        tmdb_resp = Movie.get_movie(movie_id)
        if not tmdb_resp.ok:
            raise NotOKError("TMDB raised an exception while fetching a movie's primary information")
        tmdb_resp_json = tmdb_resp.json()
        runtime: int = tmdb_resp_json["runtime"]

        lower_bound: int = runtime - 10
        upper_bound: int = runtime + 10
        return f"with_runtime.gte={lower_bound}&with_runtime.lte={upper_bound}"


parser = reqparse.RequestParser()
parser.add_argument(SimilarityParameters.ACTORS, required=False, location=('args',),
                    help="Get the movies whose first two actors overlap with the subject movie")
parser.add_argument(SimilarityParameters.GENRES, required=False, location=('args',),
                    help="Get the movies whose genres match exactly with the subject movie")
parser.add_argument(SimilarityParameters.RUNTIME, required=False, location=('args',),
                    help="Get the movies whose runtime is similar to the subject movie")
parser.add_argument('amount', required=True, type=int, location=('args',),
                    help="Get the amount of movies similar to the subject movie")



class Similar(Resource):
    """The api endpoint that represents a collection of movie resource similar to a specified, similar movie resource.

    This resource supports project requirement 2.: exactly matching genres,
    3.: similar runtime and 4.: overlapping actors by implementing the get http method.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the collection of Movie resources similar to a specific Movie resource.

        :return: The route string
        """
        return f"{Movie.route()}/similar"

    @staticmethod
    def get_credits(movie_id: int) -> requests.Response:
        """Get the crew and cast for the specified movie from the TMDB ``/movie/{movie_id}/credits`` API.

        :param movie_id: Which movie get the credits for
        :return: The TMDB response, containing the credits if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={current_app.config['API_KEY_TMDB']}")

    @staticmethod
    def get_discover_page(page: int, query_string: str) -> requests.Response:
        """Get a *page* of movies from the TMDB ``/discover/movie`` API.

        :param page: Which page to retrieve
        :return: The TMDB response, containing the list op discover movies if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={current_app.config['API_KEY_TMDB']}{query_string}&page={page}")

    @staticmethod
    def get_movie_genres() -> requests.Response:
        """Get all movie genres from the TMDB ``/genre/movie/list`` API.

        :return: The TMDB response, containing the list op movie genres if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={current_app.config['API_KEY_TMDB']}")

    @catch_unexpected_exceptions("find similar movies", True)
    @require_movie_not_deleted
    def get(self, mov_id: int):
        """The query endpoint of the collection of movies similar to the specified movie.

        :return: The similar movies
        """
        from . import movies_attributes
        args = parser.parse_args()
        supplied_valid_arg_names = [argName for argName in SimilarityParameters.accepted_parameters() if args[argName] is not None]
        remaining_movies: int = args["amount"]

        similar_movies = []
        total_pages_available: int = 1
        current_page: int = 1

        try:
            query_string: str = ""
            substring_constructors = SimilarityParameters.function_mapping()

            # Construct TMDB query string
            for keyword in supplied_valid_arg_names:
                query_substr_constructor = substring_constructors.get(keyword, None)
                if query_substr_constructor is None:
                    raise RuntimeError(f"A valid and accepted Webservices similarity parameter, '{keyword}', is missing a TMDB query substring constructor implementation")
                query_string += "&" + query_substr_constructor(mov_id)
            
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???
            # TODO Respond with the query parameters to the frontend???

            while remaining_movies > 0 and current_page <= total_pages_available:

                # Query TMDB API for similar movies
                tmdb_resp = self.get_discover_page(current_page, query_string)
                if not tmdb_resp.ok:
                    raise NotOKError("TMDB raised an exception while fetching similar movies")

                tmdb_resp_json = tmdb_resp.json()
                results = tmdb_resp_json["results"]
                results = [
                    result
                    for result in results
                    if not movies_attributes.is_deleted(result["id"])
                ]
                results = results[:remaining_movies]
                total_pages_available = tmdb_resp_json["total_pages"]

                # Bookkeeping
                remaining_movies -= len(results)
                current_page += 1

                # Append results
                similar_movies.extend(results)

            return make_response_message(E_MSG.SUCCESS, 200, result=similar_movies)
        except (JSONDecodeError, KeyError) as e:
            return make_response_error(E_MSG.ERROR, "TMDB gave an invalid or malformed response", 502)
        except NotOKError as e:
            return make_response_error(E_MSG.ERROR, str(e), 502)
