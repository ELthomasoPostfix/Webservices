from flask_restful import Resource

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
        return "movies"
