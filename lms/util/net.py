import logging

import requests

# TEST - Clean

# TEST - Type

# Return: (response, body)
def make_get(url, headers, raise_for_status = True):
    logging.debug(f"Making GET request: '%s'.", url)
    response = requests.get(url, headers = headers)

    if (raise_for_status):
        response.raise_for_status()

    body = response.text
    logging.debug("Response:\n%s", body)

    return response, body

# Return: (response, body)
def make_post(url, headers, data, raise_for_status = True):
    logging.debug("Making POST request: '%s'.", url)

    response = requests.post(url, headers = headers, data = data)

    if (raise_for_status):
        response.raise_for_status()

    body = response.text
    logging.debug("Response:\n%s", body)

    return response, body
