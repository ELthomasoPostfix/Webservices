from flask_restful import Resource


class API(Resource):
    """The api endpoint that the API resource.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the API resource.

        :return: The route string
        """
        return '/'

    def get(self):
        return "The docs for the API should be output here", 200
