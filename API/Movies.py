from typing import Literal
from flask_restful import Resource

class Movies(Resource):
    """The api endpoint that represents the collection
    of all movie resources.
    """
    @staticmethod
    def route() -> Literal:
        return "/movies/"

    def get(self):
        return "movies"
