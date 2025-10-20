import typing

import edq.util.json

import lms.model.base
import lms.util.string

class Course(lms.model.base.BaseType):
    """
    A course.
    """

    CORE_FIELDS = [
        'id', 'name',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("Course must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this course. """

        self.name: typing.Union[str, None] = name
        """ The display name of this course. """

    def to_query(self) -> 'CourseQuery':
        """ Get a query representation of this course. """

        return CourseQuery(id = self.id, name = self.name)

class CourseQuery(edq.util.json.DictConverter):
    """
    A class for the different ways one can attempt to reference an LMS course.
    In general, a course can be queried by:
     - LMS Course ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        if (id is not None):
            id = str(id)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this query. """

        self.name: typing.Union[str, None] = name
        """ The display name of this query. """

        if ((self.id is None) and (self.name is None)):
            raise ValueError("Course query is empty, it must have at least one piece of information (id, name).")

    def requires_resolution(self) -> bool:
        """
        Check if this query needs to be resolved.
        Typically, this means that the query is not just an LMS ID.
        """

        return ((self.id is None) or (self.name is not None))

    def match(self, target: typing.Union[Course, 'CourseQuery', None]) -> bool:
        """ Check if this query matches a course. """

        if (target is None):
            return False

        for field_name in ['id', 'name']:
            self_value = getattr(self, field_name, None)
            target_value = getattr(target, field_name, None)

            if (self_value is None):
                continue

            if (self_value != target_value):
                return False

        return True

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, CourseQuery)):
            return False

        # Check the ID specially.
        comparison = lms.util.string.compare_maybe_ints(self.id, other.id)
        if (comparison != 0):
            return False

        return (self.name == other.name)

    def __lt__(self, other: object) -> bool:
        if (not isinstance(other, CourseQuery)):
            return False

        # Check the ID specially.
        comparison = lms.util.string.compare_maybe_ints(self.id, other.id)
        if (comparison != 0):
            return (comparison < 0)

        if ((self.name is None) and (other.name is None)):
            return False

        if (self.name is None):
            return True

        if (other.name is None):
            return False

        return (self.name < other.name)

    def __hash__(self) -> int:
        return hash((self.id, self.name))

    def __str__(self) -> str:
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

class ResolvedCourseQuery(CourseQuery):
    """
    A CourseQuery that has been resolved (verified) from a real course instance.
    """

    def __init__(self,
            course: Course,
            **kwargs: typing.Any) -> None:
        super().__init__(id = course.id, name = course.name, **kwargs)

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

    def get_id(self) -> str:
        """ Get the ID (which must exists) for this query. """

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

        return self.id
