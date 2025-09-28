import typing

import lms.model.base

class CourseUser(lms.model.base.BaseType):
    """
    A user associated with a course, e.g., an instructor or student.
    """

    CORE_FIELDS: list[str] = ['id', 'name', 'email', 'username', 'role']
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
