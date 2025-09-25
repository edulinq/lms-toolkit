import typing

import lms.backend.canvas.backend
import lms.model.backend

def get_backend(
        server: str,
        backend_type: typing.Union[str, None] = None,
        **kwargs) -> lms.model.backend.APIBackend:
    """
    Get an instance of an API backend from the given information.
    If the backend type is not explicitly provided,
    this function will attempt to guess it from other information.
    """

    if (backend_type is None):
        backend_type = guess_backend_type(server)

    if (backend_type == lms.model.backend.BACKEND_TYPE_CANVAS):
        return lms.backend.canvas.backend.CanvasBackend(server, **kwargs)
    else:
        raise ValueError(f"Unknown backend type: '{backend_type}'. Known backend types: {lms.model.backend.BACKEND_TYPES}.")

def guess_backend_type(server: str) -> str:
    """
    Attempt to guess the backend type from a server.
    This function will raise if it cannot guess the backend type.
    """

    if ('canvas' in sevrer.lower()):
        return lms.model.backend.BACKEND_TYPE_CANVAS

    raise ValueError(f"Unable to guess backend type from server: '{server}'.")
