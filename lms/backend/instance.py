import typing

import edq.net.request
import requests

import lms.backend.blackboard.backend
import lms.backend.canvas.backend
import lms.backend.moodle.backend
import lms.model.config
import lms.model.constants
import lms.model.backend

def get_backend(
        config: lms.model.config.Config,
        **kwargs: typing.Any) -> lms.model.backend.APIBackend:
    """
    Get an instance of an API backend from the given config information.
    If the backend type is not explicitly provided,
    this function will attempt to guess it from other information.

    This function may modify the config and will pass ownership to the backend instance.
    """

    if (config.server is None):
        raise ValueError("No LMS server address provided.")

    config.server = config.server.strip()
    if (not config.server.startswith('http')):
        config.server = 'http://' + config.server

    guess_backend_type(config)
    if (config.backend_type is None):
        raise ValueError(f"Unable to guess backend type from server: '{config.server}'.")

    if (config.backend_type == lms.model.constants.BackendType.CANVAS):
        return lms.backend.canvas.backend.CanvasBackend(config = config, **kwargs)
    elif (config.backend_type == lms.model.constants.BackendType.MOODLE):
        return lms.backend.moodle.backend.MoodleBackend(config = config, **kwargs)
    elif (config.backend_type == lms.model.constants.BackendType.BLACKBOARD):
        return lms.backend.blackboard.backend.BlackboardBackend(config = config, **kwargs)
    elif (config.backend_type not in lms.model.constants.BackendType):
        raise ValueError(f"Instance creation not yet supported for backend type: '{config.backend_type.value}'.")
    else:
        raise ValueError((f"Unknown backend type: '{config.backend_type.value}'.",
                + f" Known backend types: {[choice.value for choice in lms.model.constants.OutputFormat]}."))

def guess_backend_type(
        config: lms.model.config.Config,
        **kwargs: typing.Any) -> None:
    """
    Attempt to guess the backend type from a server.
    The result of the guess (which may be None) will be placed in the passed-in config.
    """

    if (config.backend_type is not None):
        return

    if (config.server is None):
        return

    # Try looking at the URL string itself.
    config.backend_type = guess_backend_type_from_url(config.server)
    if (config.backend_type is not None):
        return

    # Finally, make a request to the server and examine the response.
    config.backend_type = guess_backend_type_from_request(config.server)

def guess_backend_type_from_request(
        server: str,
        timeout_secs: typing.Union[float, None] = None,
        ) -> typing.Union[lms.model.constants.BackendType, None]:
    """
    Attempt to guess the backend type by pinging the server.
    This function will not do any lexical analysis on the server string.
    """

    options = {
        'allow_redirects': False,
    }

    try:
        response, _ = edq.net.request.make_get(server,
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
        return lms.model.constants.BackendType.BLACKBOARD

    # Canvas sends a special header.
    if ('x-canvas-meta' in header_keys):
        return lms.model.constants.BackendType.CANVAS

    # Canvas requests that a specific cookie is set.
    if ('_normandy_session' in response.headers.get('set-cookie', '')):
        return lms.model.constants.BackendType.CANVAS

    # Moodle will try to redirect with a special header.
    if (response.headers.get('x-redirect-by', '').lower() == 'moodle'):
        return lms.model.constants.BackendType.MOODLE

    # Moodle requests that a specific cookie is set.
    if ('MoodleSession' in response.headers.get('set-cookie', '')):
        return lms.model.constants.BackendType.MOODLE

    return None

def guess_backend_type_from_url(server: str) -> typing.Union[lms.model.constants.BackendType, None]:
    """
    Attempt to guess the backend type only from a string server URL.
    This function will only do lexical analysis on the string (no HTTP requests will be made).
    """

    server = server.lower().strip()

    if ('canvas' in server):
        return lms.model.constants.BackendType.CANVAS

    if ('moodle' in server):
        return lms.model.constants.BackendType.MOODLE

    if ('blackboard' in server):
        return lms.model.constants.BackendType.BLACKBOARD

    return None
