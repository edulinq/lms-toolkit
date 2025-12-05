import re
import typing

import lms.model.courses
import lms.model.users

COURSE_ROLE_MAPPING: typing.Dict[str, lms.model.users.CourseRole] = {
    'Guest': lms.model.users.CourseRole.OTHER,
    'Student': lms.model.users.CourseRole.STUDENT,
    'Grader': lms.model.users.CourseRole.GRADER,
    'TeachingAssistant': lms.model.users.CourseRole.ADMIN,
    'Instructor': lms.model.users.CourseRole.OWNER,
}

def parse_id(text: str) -> str:
    """ Blackboard tends to put other text around their ids. """

    text = text.strip()

    match = re.match(r'^_(\d+)_\d*', text)
    if (match is not None):
        return match.group(1)

    return text

def format_id(id: int) -> str:
    """ Format a Blackboard primary ID. """

    return f"_{id}_1"

def course(data: typing.Dict[str, typing.Any]) -> lms.model.courses.Course:
    """
    Create a Blackboard course from raw data.
    """

    return lms.model.courses.Course(
        id = parse_id(data['id']),
        name = data['name'],
    )

def course_user(data: typing.Dict[str, typing.Any]) -> lms.model.users.CourseUser:
    """
    Create a Blackboard course from raw data.
    """

    user = data['user']

    return lms.model.users.CourseUser(
        id = parse_id(user['id']),
        name = user['name']['given'],
        email = user['contact']['email'],
        raw_role = data['courseRoleId'],
        role = COURSE_ROLE_MAPPING.get(data['courseRoleId'], None),
    )
