from flask_restful import Resource
from .Movies import Movies

class Movie(Resource):
    """The api endpoint that represents a single movie resource.
    """
    @staticmethod
    def route() -> str:
        """Get the route to the Movie resource.

        :return: The route string
        """
        return f"{Movies.route()}/<int:mov_id>"

    def get(self, mov_id: int):
        return f"movie {mov_id}"
