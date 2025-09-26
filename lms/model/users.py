import typing

import edq.util.json

class CourseUser(edq.util.json.DictConverter):  # type: ignore[misc]
    """
    A user associated with a course, e.g., an instructor or student.
    """

    COMMON_FIELDS: list[str] = ['id', 'name', 'email', 'username', 'role']
    """ The common fields shared across backends for this type. """

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

        self.extra_fields: typing.Dict[str, typing.Any] = kwargs.copy()
        """ Additional fields not common to all backends or explicitly used by the creating child backend. """

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, CourseUser)):
            return False

        # Check the common fields only.
        for field_name in self.COMMON_FIELDS:
            if (getattr(self, field_name) != getattr(other, field_name)):
                return False

        return True
