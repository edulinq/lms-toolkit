import datetime
import typing

import edq.util.json
import edq.util.time

import lms.util.net

DEFAULT_PAGE_SIZE = 95
HEADER_LINK = 'Link'

# TEST - Clean

# TEST - Type

def fetch_next_canvas_link(headers):
    if (HEADER_LINK not in headers):
        return None

    links = headers[HEADER_LINK].split(',')
    for link in links:
        parts = link.split(';')
        if (len(parts) != 2):
            continue

        if (parts[1].strip() != 'rel="next"'):
            continue

        return parts[0].strip().strip('<>')

    return None

# Repeatedly call make_get_request() (using a JSON body and next link) until there are no more results.
def make_get_request_list(url, headers):
    output = []

    while (url is not None):
        response, body_text = lms.util.net.make_get(url, headers)

        url = fetch_next_canvas_link(response.headers)
        new_results = edq.util.json.loads(body_text)

        for new_result in new_results:
            output.append(new_result)

    return output

def parse_timestamp(value: typing.Union[str, None]) -> typing.Union[edq.util.time.Timestamp, None]:
    """ Parse a Canvas timestamp into a common form. """

    if (value is None):
        return None

    pytime = datetime.datetime.fromisoformat(value)
    return edq.util.time.Timestamp.from_pytime(pytime)
