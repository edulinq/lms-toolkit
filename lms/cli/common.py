import typing

import lms.util.parse

def check_required_course(config: typing.Dict[str, typing.Any]) -> typing.Union[str, None]:
    """
    Fetch and ensure that a course is provided in the config.
    If no course is provided, print a message and return None.
    """

    course = lms.util.parse.optional_string(config.get('course', None))
    if (course is None):
        print('ERROR: No course has been provided.')

    return course

def check_required_assignment(config: typing.Dict[str, typing.Any]) -> typing.Union[str, None]:
    """
    Fetch and ensure that a assignment is provided in the config.
    If no assignment is provided, print a message and return None.
    """

    assignment = lms.util.parse.optional_string(config.get('assignment', None))
    if (assignment is None):
        print('ERROR: No assignment has been provided.')

    return assignment
