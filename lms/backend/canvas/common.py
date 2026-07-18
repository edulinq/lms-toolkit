import datetime
import http
import re
import typing

import html2text

import edq.net.request
import edq.util.json
import edq.util.time
import requests

DEFAULT_PAGE_SIZE: int = 95
HEADER_LINK: str = 'Link'

def fetch_next_canvas_link(response: requests.Response) -> typing.Union[str, None]:
    """
    Fetch the Canvas-style next link within the headers.
    If there is no next link, return None.
    """

    headers = response.headers

    if (HEADER_LINK not in headers):
        return None

    links = headers[HEADER_LINK].split(',')
    for link in links:
        parts = link.split(';')
        if (len(parts) != 2):
            continue

        if (parts[1].strip() != 'rel="next"'):
            continue

        return str(parts[0].strip().strip('<>'))

    return None

def make_request(
        method: str,
        url: str,
        raise_on_404: bool = False,
        json: bool = True,
        **kwargs: typing.Any) -> typing.Union[typing.Any, None]:
    """ Make a single Canvas request and return the decoded JSON body. """

    try:
        _, body_text = edq.net.request.make_request(method, url, **kwargs)
    except requests.HTTPError as ex:
        if (raise_on_404 or (ex.response is None) or (ex.response.status_code != http.HTTPStatus.NOT_FOUND)):
            raise ex

        return None

    if (not json):
        return body_text

    return edq.util.json.loads(body_text, strict = True)

def make_get_request(url: str, **kwargs: typing.Any) -> typing.Union[typing.Any, None]:
    """ Make a single Canvas GET request. """

    return make_request('GET', url, **kwargs)

def make_post_request(url: str, **kwargs: typing.Any) -> typing.Union[typing.Any, None]:
    """ Make a single Canvas POST request. """

    return make_request('POST', url, **kwargs)

def make_put_request(url: str, **kwargs: typing.Any) -> typing.Union[typing.Any, None]:
    """ Make a single Canvas PUT request. """

    return make_request('PUT', url, **kwargs)

def make_delete_request(url: str, **kwargs: typing.Any) -> typing.Union[typing.Any, None]:
    """ Make a single Canvas DELETE request. """

    return make_request('DELETE', url, **kwargs)

def make_get_request_list(
        url: str,
        headers: typing.Dict[str, typing.Any],
        data: typing.Union[typing.Dict[str, typing.Any], None] = None,
        raise_on_404: bool = False,
        ) -> typing.Union[typing.List[typing.Dict[str, typing.Any]], None]:
    """ Repeatedly call make_get_request() (using a JSON body and next link) until there are no more results. """

    output: typing.List[typing.Dict[str, typing.Any]] = []

    next_url: typing.Union[str, None] = url

    while (next_url is not None):
        try:
            response, body_text = edq.net.request.make_get(next_url, headers = headers, data = data)
        except requests.HTTPError as ex:
            if (raise_on_404 or (ex.response is None) or (ex.response.status_code != http.HTTPStatus.NOT_FOUND)):
                raise ex

            return None

        next_url = fetch_next_canvas_link(response)

        new_results = edq.util.json.loads(body_text, strict = True)
        for new_result in new_results:
            output.append(new_result)

    return output

def parse_timestamp(value: typing.Union[str, None]) -> typing.Union[edq.util.time.Timestamp, None]:
    """ Parse a Canvas-style timestamp into a common form. """

    if (value is None):
        return None

    # Parse out some cases that Python <= 3.10 cannot deal with.
    value = re.sub(r'Z$', '+00:00', value)
    value = re.sub(r'(\d\d:\d\d)(\.\d+)', r'\1', value)

    pytime = datetime.datetime.fromisoformat(value)
    return edq.util.time.Timestamp.from_pytime(pytime)

def html_to_markdown(html: typing.Union[str, None]) -> str:
    """
    Parse the text from a Canvas quiz question into markdown.
    We intend for the resulting markdown to have a little HTML as possible.
    This is an impossible task, but we want to do our best.
    """

    if (html is None):
        return ''

    converter = html2text.HTML2Text()

    converter.body_width = 0
    converter.mark_code = True

    text = converter.handle(html)
    text = text.strip()

    # Replace code tags with fences.
    text = re.sub(r'\[/?code\]', '```', text)

    # Replace placeholders (e.g., for fill in the blank questions).
    text = re.sub(r'\[(\w+?)\]', r'<placeholder>\1</placeholder>', text)

    return text
