from io import BytesIO
from flask import send_file
import marshmallow
from requests.exceptions import JSONDecodeError
from flask_restful import reqparse
from typing import List, Tuple, Set
from flask_apispec import MethodResource, marshal_with, doc

from .Movies import Movies
from .utils import catch_unexpected_exceptions
from .exceptions import NotOKTMDB, NotOKQuickchart
from .APIResponses import make_response_error, GenericResponseMessages as E_MSG, TMDBResponseMessages as E_TMDB, QuickchartResponseMessages as E_QC
from .APIClients import TMDBClient, QuickchartClient
from .schemaModels import generate_params_from_parser


class PlotParameters:
    """An enum of the parameters used by the AverageScorePlot resource to
    provide average score plots.

    For descriptions of the parameters, refer to the help argument
    specified in their addition as arguments to the reqparser below.
    """
    movie_ids = "movie_ids"

"""The query arguments passed to this endpoint facilitate
features related to constructing a barplot of average scores
for the specified list of movies.

The query parameters correspond to the required project features
in the following way:
    * PlotParameters.movie_ids: 5.

The feature numbers (i.e. 'x.') refer to the features in the
same order as they are listed in the Project Specification
section of the README
"""
parser = reqparse.RequestParser()
parser.add_argument(PlotParameters.movie_ids, type=str, required=True, location=('args',),
                    help="A comma-separated list of TMDB movie ids")


class AverageScorePlot(MethodResource):
    """The api endpoint that represents a barplot of average movie scores resource.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the barplot of average movie scores resource.

        :return: The route string
        """
        return f"{Movies.route()}/average-score-plot"

    @doc(description='A barplot of average score values',
         params=generate_params_from_parser(parser),
         content_type='application/octet-stream')
    @marshal_with(marshmallow.fields.Raw, code=(200, 400, 502))
    @catch_unexpected_exceptions("query the similar score barchart collection")
    def get(self):
        """The fetch endpoint of the average movie score barplot of a collection of Movie resources.

        Silently prunes deleted movie ids from the query string, but does respond with the
        rejected/excluded movie ids added in the 'Excluded-Movie-IDs'.

        :return: The average movie score barplot
        """
        args = parser.parse_args()
        try:
            from . import movies_attributes
            movie_ids: List[str] = args[PlotParameters.movie_ids].split(',')
            if any((movie_id != "" and not movie_id.isnumeric() for movie_id in movie_ids)):
                return make_response_error(E_MSG.ERROR, f"The {PlotParameters.movie_ids} query param should be a comma separated list of TMDB ids (positive integers)", 400)
            unique_movie_ids: Set[int] = set([int(movie_id) for movie_id in movie_ids if movie_id != ""])
            valid_movie_ids: List[int] = movies_attributes.prune_deleted_keys(unique_movie_ids)
            resolved_movie_ids: Set[int] = set()

            movies_data: List[Tuple[str, int]] = []
            for valid_movie_id in valid_movie_ids:
                tmdb_resp = TMDBClient.get_movie(valid_movie_id)
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

            quickchart_resp = QuickchartClient.get_barplot(movies_data)
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


