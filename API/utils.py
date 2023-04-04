import flask
from typing import Any, Callable
from .APIResponses import GenericResponseMessages as E_MSG, make_response_error


def catch_unexpected_exceptions(action_description: str, return_exception: bool=False):
    """A convenience wrapper that simply catches and handles the broadest class of exceptions.
    
    This wrapper condences the boilerplate of handling the broadest class of exceptions,
    namely Exception, in a structured way to a single line. Its use is recommended for the
    sake of elegance and, more importantly, avoiding code duplication while also somewhat
    enforcing a uniform return format in the case of unexpected errors.

    The *action_description* parameter should match the following sentence structure: "failed to <action_description>"

    e.g. ::

        @catch_unexpected_exceptions("add numbers")
        def add(x: int, y: int):
            raise RuntimeError("bogus add exception")
            return x + y

        @catch_unexpected_exceptions("sub numbers", return_exception=True)
        def sub(x: int, y: int):
            raise RuntimeError("bogus sub exception")
            return x + y


    .. function:: add(x: int, y: int)
    .. function:: sub(x: int, y: int)
    In the previous code, calling :func:`add` would result in the following response body: ::
    
        {
            "error": "Unexpected error, failed to add numbers",
            "message": "Encountered an unexpected exception"
        }
    
    And calling :func:`sub` would result in the following response body: ::

        {
            "error": "Unexpected error, failed to add numbers",
            "exception": "bogus sub exception",
            "message": "Encountered an unexpected exception"
        }

    :param action_description: The description of the action that is being interrupted by the unexpected exception
    :param return_exception: Whether to return the exception's error message along with the response, under 'exception' in the body
    :return: The decorator
    """
    def decorator(http_method: Callable):
        # The decorator is called instead of the wrapped
        # function, but flask restful expects the called
        # method to have an http verb (get, post, put,
        # delete, ...) as its name.
        decorator.__name__ = http_method.__name__
        
        def wrapper(*args, **kwargs) -> flask.Response | Any:
            try:
                return http_method(*args, **kwargs)
            except Exception as e:
                if return_exception:
                    return make_response_error(E_MSG.UNEXPECTED, f"Unexpected error, failed to {action_description}", 500,
                                               exception=str(e))
                return make_response_error(E_MSG.UNEXPECTED, f"Unexpected error, failed to {action_description}", 500)

        return wrapper
    return decorator

def require_movie_not_deleted(http_method: Callable):
    """A convenience wrapper that requires a `mov_id` function paramter to not be part of the deleted movies.

    This wrapper condences the boilerplate of handling checking whether the `mov_id` parameter,
    of the wrapped function is marked as deleted or not. Its use is recommended for the sake of
    elegance and, more importantly, avoiding code duplication while also somewhat enforcing a
    uniform return format in the case of the movie being deleted.

    e.g. ::

        @require_movie_not_deleted
        def get_movie_info(mov_id: int):
            return {
                "title": "mov_" + str(mov_id),
                "id": mov_id
            }

    .. function:: get_movie_info(mov_id: int)
    In the previous code, imagine that the movies `1, 2, 3` were deleted. Then, calling :func:`get_movie_info(2)` would result in the following response body with a status code of 404: ::

        {
            "error": "This movie resource does not exist",
            "message": "Something went wrong"
        }

    :param http_method: The wrapped http method
    :return: The decorator
    """
    def wrapper(*args, **kwargs):
        # The decorator is called instead of the wrapped
        # function, but flask restful expects the called
        # method to have an http verb (get, post, put,
        # delete, ...) as its name.
        from . import movies_attributes
        mov_id: int = kwargs["mov_id"]
        if mov_id in movies_attributes and movies_attributes.is_deleted(mov_id):
            return make_response_error(E_MSG.ERROR, "This movie resource does not exist", 404)

        return http_method(*args, **kwargs)

    wrapper.__name__ = http_method.__name__
    return wrapper
