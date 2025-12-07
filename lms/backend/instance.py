import typing

import edq.util.net
import requests

import lms.backend.blackboard.backend
import lms.backend.canvas.backend
import lms.backend.moodle.backend
import lms.model.constants
import lms.model.backend

def get_backend(
        server: typing.Union[str, None] = None,
        backend_type: typing.Union[str, None] = None,
        **kwargs: typing.Any) -> lms.model.backend.APIBackend:
    """
    Get an instance of an API backend from the given information.
    If the backend type is not explicitly provided,
    this function will attempt to guess it from other information.
    """

    if (server is None):
        raise ValueError("No LMS server address provided.")

    server = server.strip()
    if (not server.startswith('http')):
        server = 'http://' + server

    backend_type = guess_backend_type(server, backend_type = backend_type)
    if (backend_type is None):
        raise ValueError(f"Unable to guess backend type from server: '{server}'.")

    if (backend_type == lms.model.constants.BACKEND_TYPE_CANVAS):
        return lms.backend.canvas.backend.CanvasBackend(server, **kwargs)

    if (backend_type == lms.model.constants.BACKEND_TYPE_MOODLE):
        return lms.backend.moodle.backend.MoodleBackend(server, **kwargs)

    if (backend_type == lms.model.constants.BACKEND_TYPE_BLACKBOARD):
        return lms.backend.blackboard.backend.BlackboardBackend(server, **kwargs)

    if (backend_type in lms.model.constants.BACKEND_TYPES):
        raise ValueError(f"Instance creation not yet supported for backend type: '{backend_type}'.")

    raise ValueError(f"Unknown backend type: '{backend_type}'. Known backend types: {lms.model.constants.BACKEND_TYPES}.")

def guess_backend_type(
        server: typing.Union[str, None] = None,
        backend_type: typing.Union[str, None] = None,
        **kwargs: typing.Any) -> typing.Union[str, None]:
    """
    Attempt to guess the backend type from a server.
    This function will return None it cannot guess the backend type.
    """

    if (backend_type is not None):
        return backend_type

    if (server is None):
        return None

    # Try looking at the URL string itself.
    backend_type = guess_backend_type_from_url(server)
    if (backend_type is not None):
        return backend_type

    # Make a request to the server and examine the response.
    backend_type = guess_backend_type_from_request(server)
    if (backend_type is not None):
        return backend_type

    return None

def guess_backend_type_from_request(server: str, timeout_secs: float = edq.util.net.DEFAULT_REQUEST_TIMEOUT_SECS) -> typing.Union[str, None]:
    """
    Attempt to guess the backend type by pinging the server.
    This function will not do any lexical analysis on the server string.
    """

    options = {
        'allow_redirects': False,
    }

    try:
        response, _ = edq.util.net.make_get(server,
                raise_for_status = False,
                timeout_secs = timeout_secs,
                additional_requests_options = options)
    except requests.exceptions.ConnectionError:
        return None
    except requests.exceptions.Timeout:
        return None

    header_keys = [key.lower() for key in response.headers.keys()]

    # Blackboard sends a special header.
    if ('x-blackboard-product' in header_keys):
        return lms.model.constants.BACKEND_TYPE_BLACKBOARD

    # Canvas sends a special header.
    if ('x-canvas-meta' in header_keys):
        return lms.model.constants.BACKEND_TYPE_CANVAS

    # Canvas requests that a specific cookie is set.
    if ('_normandy_session' in response.headers.get('set-cookie', '')):
        return lms.model.constants.BACKEND_TYPE_CANVAS

    # Moodle will try to redirect with a special header.
    if (response.headers.get('x-redirect-by', '').lower() == 'moodle'):
        return lms.model.constants.BACKEND_TYPE_MOODLE

    # Moodle requests that a specific cookie is set.
    if ('MoodleSession' in response.headers.get('set-cookie', '')):
        return lms.model.constants.BACKEND_TYPE_MOODLE

    return None

def guess_backend_type_from_url(server: str) -> typing.Union[str, None]:
    """
    Attempt to guess the backend type only from a string server URL.
    This function will only do lexical analysis on the string (no HTTP requests will be made).
    """

    server = server.lower().strip()

    if ('canvas' in server):
        return lms.model.constants.BACKEND_TYPE_CANVAS

    if ('moodle' in server):
        return lms.model.constants.BACKEND_TYPE_MOODLE

    if ('blackboard' in server):
        return lms.model.constants.BACKEND_TYPE_BLACKBOARD

    return None
