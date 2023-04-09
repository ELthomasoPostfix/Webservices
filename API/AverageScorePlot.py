from io import BytesIO
import requests
from flask import send_file
from requests.exceptions import JSONDecodeError
from flask_restful import Resource, reqparse
from typing import List, Tuple, Set

from .Movies import Movies
from .Movie import Movie
from .utils import catch_unexpected_exceptions
from .exceptions import NotOKTMDB, NotOKQuickchart
from .APIResponses import make_response_message, make_response_error, GenericResponseMessages as E_MSG, TMDBResponseMessages as E_TMDB, QuickchartResponseMessages as E_QC


"""The query arguments passed to this endpoint facilitate
features related to constructing a barplot of average scores
for the specified list of movies.

The query parameters correspond to the required project features
in the following way:
    * movie_ids: 5.

The feature numbers (i.e. 'x.') refer to the features in the
same order as they are listed in the Project Specification
section of the README
"""
parser = reqparse.RequestParser()
parser.add_argument("movie_ids", type=str, required=True, location=('args',),
                    help="A comma-separated list of TMDB movie ids")


class AverageScorePlot(Resource):
    """The api endpoint that represents a barplot of average movie scores resource.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the barplot of average movie scores resource.

        :return: The route string
        """
        return f"{Movies.route()}/average-score-plot"

    @staticmethod
    def get_barplot(movies_data: List[Tuple[str, int]]) -> requests.Response:
        """Get a barplot from the quickchart ``/chart`` API.
        
        :param movies_data: The movies' data to plot, of the format `[ (label, avg. score), ...]`
        :return: The quickchart response, containing the barplot if successful
        """
        chart: dict = {
            "type": "bar",
            "data": {
                "labels": [ data[0] for data in movies_data ],
                "datasets": [
                    {
                        "label": 'Vote Avg.',
                        "data": [ data[1] for data in movies_data ]
                    }
                ]
            }
        }
        return requests.get(f"https://quickchart.io/chart?c={chart}")

    @catch_unexpected_exceptions("query the similar score barchart collection", True)
    def get(self):
        """The fetch endpoint of the average movie score barplot of a collection of Movie resources.

        Silently prunes deleted movie ids from the query string.

        :return: The average movie score barplot
        """
        args = parser.parse_args()
        movie_ids_param_name: str = "movie_ids"
        try:
            from . import movies_attributes
            movie_ids: List[str] = args[movie_ids_param_name].split(',')
            if any((movie_id != "" and not movie_id.isnumeric() for movie_id in movie_ids)):
                return make_response_error(E_MSG.ERROR, f"The {movie_ids_param_name} query param should be a comma separated list of TMDB ids (positive integers)", 400)
            unique_movie_ids: Set[int] = set([int(movie_id) for movie_id in movie_ids if movie_id != ""])
            valid_movie_ids: List[int] = movies_attributes.prune_deleted_keys(unique_movie_ids)
            resolved_movie_ids: Set[int] = set()

            movies_data: List[Tuple[str, int]] = []
            for valid_movie_id in valid_movie_ids:
                tmdb_resp = Movie.get_movie(valid_movie_id)
                tmdb_resp_json = tmdb_resp.json()

                if tmdb_resp.status_code == 404:
                    continue

                if not tmdb_resp.ok:
                    raise NotOKTMDB()

                resolved_movie_ids.add(valid_movie_id)
                movies_data.append((
                    f"{tmdb_resp_json['title']} ({tmdb_resp_json['id']})",
                    tmdb_resp_json["vote_average"]
                ))

            quickchart_resp = AverageScorePlot.get_barplot(movies_data)
            barchart_file: BytesIO = BytesIO(quickchart_resp.content)

            if not quickchart_resp.ok:
                raise NotOKQuickchart()

            response = send_file(barchart_file, mimetype="image/webp")
            response.headers["Excluded-Movie-IDs"] = ','.join([str(id) for id in set(unique_movie_ids).difference(resolved_movie_ids)])
            return response
        except JSONDecodeError as e:
            return make_response_error(E_MSG.ERROR, E_TMDB.ERROR_JSON_DECODE, 502)
        except NotOKTMDB as e:
            return make_response_error(E_MSG.ERROR, E_TMDB.NOT_OK, 502)
        except NotOKQuickchart as e:
            return make_response_error(E_MSG.ERROR, E_QC.NOT_OK, 502)


