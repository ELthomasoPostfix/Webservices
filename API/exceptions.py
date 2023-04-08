"""
This file contains custom errors for use in the Webservices API.
"""

import requests


class NotOKError(requests.HTTPError):
    """A generic error representing an exception to be thrown
    in case a `requests.Response.ok` property is false."""
    pass


class NotOKTMDB(NotOKError):
    """A specification of a NotOKError for the TMDB API"""
    pass


class NotOKQuickchart(NotOKError):
    """A specification of a NotOKError for the quickchart API"""
    pass
