import enum
import typing

import lms.model.base
import lms.model.query

class UserQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS user.
    In general, a user can be queried by:
     - LMS User ID (`id`)
     - Email (`email`)
     - Full Name (`name`)
     - f"{email} ({id})"
     - f"{name} ({id})"
    """

    _include_email = True

class ResolvedUserQuery(lms.model.query.ResolvedBaseQuery, UserQuery):
    """
    A UserQuery that has been resolved (verified) from a real user instance.
    """

    _include_email = True

    def __init__(self,
            user: 'ServerUser',
            **kwargs: typing.Any) -> None:
        super().__init__(id = user.id, name = user.name, email = user.email, **kwargs)

class CourseRole(enum.Enum):
    """
    Different roles a user can have in a course.
    LMSs represent this information very differently, so this is only a general collection of roles.
    """

    OTHER = 'other'
    STUDENT = 'student'
    GRADER = 'grader'
    ADMIN = 'admin'
    OWNER = 'owner'

    def __str__(self) -> str:
        return str(self.value)

class ServerUser(lms.model.base.BaseType):
    """
    A user associated with an LMS server.
    """

    CORE_FIELDS = ['id', 'name', 'email']
    """ The common fields shared across backends for this type. """

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            email: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("User must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this user. """

        self.name: typing.Union[str, None] = name
        """ The display name of this user. """

        self.email: typing.Union[str, None] = email
        """ The email address of this user. """

    def to_query(self) -> ResolvedUserQuery:
        """ Get a query representation of this user. """

        return ResolvedUserQuery(self)

class CourseUser(ServerUser):
    """
    A user associated with a course, e.g., an instructor or student.
    """

    CORE_FIELDS = ServerUser.CORE_FIELDS + ['role']
    """ The common fields shared across backends for this type. """

    def __init__(self,
            role: typing.Union[CourseRole, None] = None,
            raw_role: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.role: typing.Union[CourseRole, None] = role
        """ The role of this user within this course (e.g., owner, student). """

        self.raw_role: typing.Union[str, None] = raw_role
        """
        The raw role string from the LMS.
        This may not translate nicely into one of our known roles.
        """

    def is_student(self) -> bool:
        """
        Check if this course user is a student (and therefore be included in graded components like gradebooks).
        Backends should implement this method.
        """

        return (self.role == CourseRole.STUDENT)
