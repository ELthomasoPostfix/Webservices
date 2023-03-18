from typing import Literal
from flask_restful import Resource
from .Movies import Movies

class Movie(Resource):
    """The api endpoint that represents a single movie resource.
    """
    @staticmethod
    def route() -> Literal:
        return f"{Movies.route()}/<int:mov_id>"

    def get(self, mov_id: int):
        return f"movie {mov_id}"
