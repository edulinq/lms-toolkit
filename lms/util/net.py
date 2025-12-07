"""
Utilities for network and HTTP.
"""

import typing
import urllib.parse

import edq.util.json
import requests

import lms.model.constants

CANVAS_CLEAN_REMOVE_CONTENT_KEYS: typing.List[str] = [
    'created_at',
    'ics',
    'last_activity_at',
    'lti_context_id',
    'preview_url',
    'secure_params',
    'total_activity_time',
    'updated_at',
    'url',
    'uuid',
]
""" Keys to remove from Canvas content. """

BLACKBOARD_CLEAN_REMOVE_CONTENT_KEYS: typing.List[str] = [
    'created',
    'modified',
]
""" Keys to remove from Blackboard content. """

BLACKBOARD_CLEAN_REMOVE_HEADERS: typing.Set[str] = {
    'access-control-allow-origin',
    'content-encoding',
    'content-language',
    'expires',
    'last-modified',
    'p3p',
    'pragma',
    'strict-transport-security',
    'transfer-encoding',
    'vary',
    'x-blackboard-xsrf',
}
""" Keys to remove from Blackboard content. """

def clean_lms_response(response: requests.Response, body: str) -> str:
    """
    A ResponseModifierFunction that attempt to identify
    if the requests comes from a Learning Management System (LMS),
    and clean the response accordingly.
    """

    # Check the standard LMS Toolkit backend header.
    backend_type = response.headers.get(lms.model.constants.HEADER_KEY_BACKEND, '').lower()

    if (backend_type == lms.model.constants.BACKEND_TYPE_CANVAS):
        return clean_canvas_response(response, body)

    if (backend_type == lms.model.constants.BACKEND_TYPE_MOODLE):
        return clean_moodle_response(response, body)

    # Try looking inside the header keys.
    for key in response.headers:
        key = key.lower().strip()

        if ('blackboard' in key):
            return clean_blackboard_response(response, body)

        if ('canvas' in key):
            return clean_canvas_response(response, body)

        if ('moodle' in key):
            return clean_moodle_response(response, body)

    return body

def clean_blackboard_response(response: requests.Response, body: str) -> str:
    """
    See clean_lms_response(), but specifically for the Blackboard LMS.
    This function will:
     - Call _clean_base_response().
     - Remove specific headers.
    """

    body = _clean_base_response(response, body)

    # Work on both request and response headers.
    for headers in [response.headers, response.request.headers]:
        for key in list(headers.keys()):
            if (key.strip().lower() in BLACKBOARD_CLEAN_REMOVE_HEADERS):
                headers.pop(key, None)

    # Most blackboard responses are JSON.
    try:
        data = edq.util.json.loads(body, strict = True)
    except Exception:
        # Response is not JSON.
        return body

    # Remove any content keys.
    _recursive_remove_keys(data, set(BLACKBOARD_CLEAN_REMOVE_CONTENT_KEYS))

    # Convert body back to a string.
    body = edq.util.json.dumps(data)

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
        data = edq.util.json.loads(body, strict = True)
    except Exception:
        # Response is not JSON.
        return body

    # Remove any content keys.
    _recursive_remove_keys(data, set(CANVAS_CLEAN_REMOVE_CONTENT_KEYS))

    # Remove special fields.

    if ('submissions/update_grades' in response.request.url):
        data.pop('id', None)

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

def _clean_base_response(response: requests.Response, body: str,
        keep_headers: typing.Union[typing.List[str], None] = None) -> str:
    """
    Do response cleaning that is common amongst all backend types.
    This function will:
     - Remove X- headers.
    """

    # Index requests are generally for identification, and we use headers.
    path = urllib.parse.urlparse(response.request.url).path.strip()
    if (path in ['', '/']):
        body = ''

    for key in list(response.headers.keys()):
        key = key.strip().lower()
        if ((keep_headers is not None) and (key in keep_headers)):
            continue

        if (key.startswith('x-')):
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

def parse_cookies(
        text_cookies: typing.Union[str, None],
        strip_key_prefix: bool = True,
        ) -> typing.Dict[str, typing.Any]:
    """ Parse cookies out of a text string. """

    cookies: typing.Dict[str, typing.Any] = {}

    if (text_cookies is None):
        return cookies

    text_cookies = text_cookies.strip()
    if (len(text_cookies) == 0):
        return cookies

    for cookie in text_cookies.split('; '):
        parts = cookie.split('=', maxsplit = 1)

        key = parts[0].lower()

        if (strip_key_prefix):
            key = key.split(', ')[-1]

        if (len(parts) == 1):
            cookies[key] = True
        else:
            cookies[key] = parts[1]

    return cookies
