"""
Utilities for network and HTTP.
"""

import json
import typing

import requests

import edq.util.json

CANVAS_CLEAN_REMOVE_CONTENT_KEYS: typing.List[str] = [
    'last_activity_at',
    'total_activity_time',
    'updated_at',
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

    return body

def clean_canvas_response(response: requests.Response, body: str) -> str:
    """
    See clean_lms_response(), but specifically for the Canvas LMS.
    This function will:
     - Remove X- headers.
     - Remove content keys: [last_activity_at, total_activity_time]
    """

    for key in list(response.headers.keys()):
        if (key.strip().lower().startswith('x-')):
            response.headers.pop(key, None)

    # Most canvas responses are JSON.
    try:
        data = edq.util.json.loads(body)
    except json.JSONDecodeError:
        # Response is not JSON.
        return body

    # Remove any content keys.
    _recursive_remove_keys(data, set(CANVAS_CLEAN_REMOVE_CONTENT_KEYS))

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

    return body

def _recursive_remove_keys(data: typing.Any, remove_keys: typing.Set[str]) -> None:
    """
    Recursively descend through the given and remove any instance to the given key from any dictionaries.
    The data should only be simple types (POD, dicts, lists, tuples).
    """

    if (isinstance(data, (list, tuple))):
        for item in data:
            _recursive_remove_keys(item, remove_keys)

        return

    if (isinstance(data, dict)):
        for key in list(data.keys()):
            if (key in remove_keys):
                del data[key]
            else:
                _recursive_remove_keys(data[key], remove_keys)

        return
