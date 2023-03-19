from flask_restful import Resource, reqparse

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
    """The api endpoint that represents the collection
    of all movie resources.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Movies collection of Movie resources.

        :return: The route string
        """
        return "/movies"

    def get(self):
        args = parser.parse_args()

        popular: int | None = args[MoviesParameters.popular]
        result: dict = dict()

        if popular is not None:
            assert popular >= 0, f"The {MoviesParameters.popular} parameter may not be negative"
            result[MoviesParameters.popular] = [i for i in range(popular)]

        return result
