import enum
import typing

import lms.model.base
import lms.model.query

class UserQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS user.
    In general, a user can be queried by:
     - LMS User ID (`id`)
     - Student ID (`student_id`)
     - Email (`email`)
     - Full Name (`name`)
     - f"{email} ({id})"
     - f"{name} ({id})"
    """

    _include_email = True

    def match(self, target: typing.Union[typing.Any, 'UserQuery', None]) -> bool:
        """
        Check if this query matches the given target.
        Extends the base match to also check the query's name against the target's student_id,
        allowing users to look up users by student ID without needing a separate field.
        """

        if (target is None):
            return False

        # Check non-name fields normally.
        for field_name in ['id', 'email']:
            self_value = getattr(self, field_name, None)
            target_value = getattr(target, field_name, None)

            if (self_value is None):
                continue

            if (self_value != target_value):
                return False

        # Check name: also allow matching against target's student_id.
        if (self.name is not None):
            target_name = getattr(target, 'name', None)
            target_student_id = getattr(target, 'student_id', None)
            if ((self.name != target_name) and (self.name != target_student_id)):
                return False

        return True

class ResolvedUserQuery(lms.model.query.ResolvedBaseQuery, UserQuery):
    """
    A UserQuery that has been resolved (verified) from a real user instance.
    """

    _include_email = True

    def __init__(self,
            user: 'ServerUser',
            **kwargs: typing.Any) -> None:
        super().__init__(id = user.id, name = user.name, email = user.email,
                student_id = user.student_id, **kwargs)

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
            student_id: typing.Union[str, None] = None,
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

        self.student_id: typing.Union[str, None] = student_id
        """ The student/institutional identifier for this user. """

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
