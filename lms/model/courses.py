import typing

import lms.model.base
import lms.model.query

class CourseQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS course.
    In general, a course can be queried by:
     - LMS Course ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedCourseQuery(lms.model.query.ResolvedBaseQuery, CourseQuery):
    """
    A CourseQuery that has been resolved (verified) from a real course instance.
    """

    _include_email = False

    def __init__(self,
            course: 'Course',
            **kwargs: typing.Any) -> None:
        super().__init__(id = course.id, name = course.name, **kwargs)

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

    def to_query(self) -> ResolvedCourseQuery:
        """ Get a query representation of this course. """

        return ResolvedCourseQuery(self)
