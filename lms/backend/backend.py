import typing

import lms.backend.canvas.backend
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

    if (backend_type == lms.model.constants.BACKEND_TYPE_CANVAS):
        return lms.backend.canvas.backend.CanvasBackend(server, **kwargs)

    raise ValueError(f"Unknown backend type: '{backend_type}'. Known backend types: {lms.model.constants.BACKEND_TYPES}.")

def guess_backend_type(
        server: typing.Union[str, None] = None,
        backend_type: typing.Union[str, None] = None,
        ) -> str:
    """
    Attempt to guess the backend type from a server.
    This function will raise if it cannot guess the backend type.
    """

    if (backend_type is not None):
        return backend_type

    if (server is not None):
        if ('canvas' in server.lower()):
            return lms.model.constants.BACKEND_TYPE_CANVAS

    raise ValueError(f"Unable to guess backend type from server: '{server}'.")
