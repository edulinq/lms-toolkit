import datetime
import typing

import edq.util.json
import edq.util.net
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

def make_get_request_list(
        url: typing.Union[str, None],
        headers: typing.Dict[str, typing.Any],
        ) -> typing.List[typing.Dict[str, typing.Any]]:
    """ Repeatedly call make_get_request() (using a JSON body and next link) until there are no more results. """

    output = []

    while (url is not None):
        response, body_text = edq.util.net.make_get(url, headers = headers)

        url = fetch_next_canvas_link(response)
        new_results = edq.util.json.loads(body_text)

        for new_result in new_results:
            output.append(new_result)

    return output

def parse_timestamp(value: typing.Union[str, None]) -> typing.Union[edq.util.time.Timestamp, None]:
    """ Parse a Canvas-style timestamp into a common form. """

    if (value is None):
        return None

    pytime = datetime.datetime.fromisoformat(value)
    return edq.util.time.Timestamp.from_pytime(pytime)
