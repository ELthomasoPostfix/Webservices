import requests

from flask_restful import current_app
from typing import List, Tuple


class TMDBClient:
    """A simple TMDB client to make API calls to the TMDB v3 API.

    No instance of this class is required, as the API key is implicitly
    taken directly from the app config. This class purely provides
    static methods to access the TMDB API.
    
    This custom class is absolutely necessary instead of a package
    because I forgot API client packages exist.
    """
    @staticmethod
    def get_movie(movie_id: int) -> requests.Response:
        """Get the primary information about a movie from the TMDB ``/movie/{movie_id}`` API.

        :param movie_id: Which movie's information to retrieve
        :return: The TMDB response, containing the requested movie if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={current_app.config['API_KEY_TMDB']}")

    @staticmethod
    def get_popular_page(page: int) -> requests.Response:
        """Get a *page* of popular movies from the TMDB ``/movie/popular`` API.
        
        :param page: Which page to retrieve
        :return: The TMDB response, containing the list op popular movies if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/movie/popular?page={page}&api_key={current_app.config['API_KEY_TMDB']}")

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

        Note that this function specifically fetches en-US translations.
        If a movie does not have one, then they may not show up in the query
        results.

        :param page: Which page to retrieve
        :param query_string: A string of query parameters of the TMDB discover API, must start with an '&'
        :return: The TMDB response, containing the list op discover movies if successful
        """
        language: str = "en-US"
        return requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={current_app.config['API_KEY_TMDB']}{query_string}&page={page}&language={language}")

    @staticmethod
    def get_movie_genres() -> requests.Response:
        """Get all movie genres from the TMDB ``/genre/movie/list`` API.

        :return: The TMDB response, containing the list op movie genres if successful
        """
        return requests.get(f"https://api.themoviedb.org/3/genre/movie/list?api_key={current_app.config['API_KEY_TMDB']}")


class QuickchartClient:
    """A simple quickchart client to make API calls to the quickchart API.

    No instance of this class is required, as no API key required.
    This class purely provides static methods to access the quickchart API.
    
    This custom class is absolutely necessary instead of a package
    because I forgot API client packages exist.
    """
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
