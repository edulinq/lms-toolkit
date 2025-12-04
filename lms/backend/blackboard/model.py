import re
import typing

import lms.model.courses

def parse_id(text: str) -> str:
    """ Blackboard tends to put other text around their ids. """

    text = text.strip()

    match = re.match(r'^_(\d+)_\d*', text)
    if (match is not None):
        return match.group(1)

    return text

def course(data: typing.Dict[str, typing.Any]) -> lms.model.courses.Course:
    """
    Create a Blackboard course from raw data.
    """

    return lms.model.courses.Course(
        id = parse_id(data['id']),
        name = data['name'],
    )
