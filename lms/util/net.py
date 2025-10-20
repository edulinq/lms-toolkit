"""
Utilities for network and HTTP.
"""

import typing

import requests

import edq.util.json

CANVAS_CLEAN_REMOVE_CONTENT_KEYS: typing.List[str] = [
    'created_at',
    'ics',
    'last_activity_at',
    'lti_context_id',
    'secure_params',
    'total_activity_time',
    'updated_at',
    'uuid',
]
""" Keys to remove from Canvas content. """

def clean_lms_response(response: requests.Response, body: str) -> str:
    """
    A ResponseModifierFunction that attempt to identify
    if the requests comes from a Learning Management System (LMS),
    and clean the response accordingly.
    """

    for key in response.headers:
        key = key.lower().strip()

        if ('canvas' in key):
            return clean_canvas_response(response, body)

        if ('moodle' in key):
            return clean_moodle_response(response, body)

    return body

def clean_canvas_response(response: requests.Response, body: str) -> str:
    """
    See clean_lms_response(), but specifically for the Canvas LMS.
    This function will:
     - Call _clean_base_response().
     - Remove content keys: [last_activity_at, total_activity_time]
    """

    body = _clean_base_response(response, body)

    # Most canvas responses are JSON.
    try:
        data = edq.util.json.loads(body)
    except Exception:
        # Response is not JSON.
        return body

    # Remove any content keys.
    _recursive_remove_keys(data, set(CANVAS_CLEAN_REMOVE_CONTENT_KEYS))

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

    return body

def clean_moodle_response(response: requests.Response, body: str) -> str:
    """
    See clean_lms_response(), but specifically for the Moodle LMS.
    This function will:
     - Call _clean_base_response().
    """

    body = _clean_base_response(response, body)

    return body

def _clean_base_response(response: requests.Response, body: str) -> str:
    """
    Do response cleaning that is common amonst all backend types.
    This function will:
     - Remove X- headers.
    """

    for key in list(response.headers.keys()):
        if (key.strip().lower().startswith('x-')):
            response.headers.pop(key, None)

    return body

def _recursive_remove_keys(data: typing.Any, remove_keys: typing.Set[str]) -> None:
    """
    Recursively descend through the given and remove any instance to the given key from any dictionaries.
    The data should only be simple types (POD, dicts, lists, tuples).
    """

    if (isinstance(data, (list, tuple))):
        for item in data:
            _recursive_remove_keys(item, remove_keys)
    elif (isinstance(data, dict)):
        for key in list(data.keys()):
            if (key in remove_keys):
                del data[key]
            else:
                _recursive_remove_keys(data[key], remove_keys)
