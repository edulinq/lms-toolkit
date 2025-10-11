import typing

import edq.util.json

import lms.model.base

class ServerUser(lms.model.base.BaseType):
    """
    A user associated with an LMS server.
    """

    CORE_FIELDS = ['id', 'name', 'email', 'username']
    """ The common fields shared across backends for this type. """

    def __init__(self,
            id: typing.Union[str, None] = None,
            email: typing.Union[str, None] = None,
            username: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("User must have an id.")

        self.id: str = id
        """ The LMS's identifier for this user. """

        self.name: typing.Union[str, None] = name
        """ The display name of this user. """

        self.email: typing.Union[str, None] = email
        """ The email address of this user. """

        self.username: typing.Union[str, None] = username
        """ The username for this user (often overlaps with email). """

    def to_query(self) -> 'UserQuery':
        """ Get a query representation of this user. """

        return UserQuery(id = self.id, name = self.name, email = self.email)

class CourseUser(ServerUser):
    """
    A user associated with a course, e.g., an instructor or student.
    """

    CORE_FIELDS = ServerUser.CORE_FIELDS + ['role']
    """ The common fields shared across backends for this type. """

    def __init__(self,
            role: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.role: typing.Union[str, None] = role
        """ The role of this user within this course (e.g., instructor, student). """

class UserQuery(edq.util.json.DictConverter):
    """
    A class for the different ways one can attempt to reference an LMS user.
    In general, a user can be queried by:
     - LMS User ID (`id`)
     - Email (`email`)
     - Full Name (`name`)
     - f"{email} ({id})"
     - f"{name} ({id})"
    """

    def __init__(self,
            id: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            email: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this query. """

        self.name: typing.Union[str, None] = name
        """ The display name of this query. """

        self.email: typing.Union[str, None] = email
        """ The email address of this query. """

        if ((self.id is None) and (self.name is None) and (self.email is None)):
            raise ValueError("User query is empty, it must have at least one piece of information (id, email, name).")

    def requires_resolution(self) -> bool:
        """
        Check if this query needs to be resolved.
        Typically, this means that the query is not just an LMS ID.
        """

        return ((self.id is None) or (self.name is not None) or (self.email is not None))

    def match(self, target: typing.Union[ServerUser, 'UserQuery', None]) -> bool:
        """ Check if this query matches a user. """

        if (target is None):
            return False

        for field_name in ['id', 'name', 'email']:
            self_value = getattr(self, field_name, None)
            target_value = getattr(target, field_name, None)

            if (self_value is None):
                continue

            if (self_value != target_value):
                return False

        return True

    def __str__(self) -> str:
        text = self.email
        if (text is None):
            text = self.name

        if (self.id is not None):
            if (text is not None):
                text = f"{text} ({self.id})"
            else:
                text = self.id

        if (text is None):
            return '<unknown>'

        return text

    def _to_text(self) -> str:
        """ Represent this query as a string. """

        return str(self)
