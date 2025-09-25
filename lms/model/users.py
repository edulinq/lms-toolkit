import typing

import edq.util.json

class CourseUser(edq.util.json.DictConverter):
    """
    A user associated with a course, e.g., an instructor or student.
    """

    def __init__(self,
            id: typing.Union[str, None] = None,
            email: typing.Union[str, None] = None,
            username: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            role: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this user. """

        self.name: typing.Union[str, None] = name
        """ The display name of this user. """

        self.email: typing.Union[str, None] = email
        """ The email address of this user. """

        self.username: typing.Union[str, None] = username
        """ The username for this user (often overlaps with email. """

        self.role: typing.Union[str, None] = role
        """ The role of this user within this course (e.g., instructor, student). """

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, CourseUser)):
            return False

        self_tuple = (self.id, self.name, self.email, self.username, self.role)
        other_tuple = (other.id, other.name, other.email, other.username, other.role)

        return (self_tuple == other_tuple)
