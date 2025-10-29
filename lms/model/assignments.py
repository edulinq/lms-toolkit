import typing

import edq.util.time

import lms.model.base
import lms.model.query

class AssignmentQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS assignment.
    In general, an assignment can be queried by:
     - LMS Assignment ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedAssignmentQuery(lms.model.query.ResolvedBaseQuery, AssignmentQuery):
    """
    A AssignmentQuery that has been resolved (verified) from a real assignment instance.
    """

    _include_email = False

    def __init__(self,
            assignment: 'Assignment',
            **kwargs: typing.Any) -> None:
        super().__init__(id = assignment.id, name = assignment.name, **kwargs)

class Assignment(lms.model.base.BaseType):
    """
    An assignment within a course.
    """

    CORE_FIELDS = [
        'id', 'name', 'description',
        'open_date', 'close_date', 'due_date',
        'points_possible',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            description: typing.Union[str, None] = None,
            open_date: typing.Union[edq.util.time.Timestamp, None] = None,
            close_date: typing.Union[edq.util.time.Timestamp, None] = None,
            due_date: typing.Union[edq.util.time.Timestamp, None] = None,
            points_possible: typing.Union[float, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("Assignment must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this assignment. """

        self.name: typing.Union[str, None] = name
        """ The display name of this assignment. """

        self.description: typing.Union[str, None] = description
        """ The description of this assignment. """

        self.open_date: typing.Union[edq.util.time.Timestamp, None] = open_date
        """ The datetime that this assignment becomes open at. """

        self.close_date: typing.Union[edq.util.time.Timestamp, None] = close_date
        """ The datetime that this assignment becomes close at. """

        self.due_date: typing.Union[edq.util.time.Timestamp, None] = due_date
        """ The datetime that this assignment is due at. """

        self.points_possible: typing.Union[float, None] = points_possible
        """ The maximum number of points possible for this assignment. """

    def to_query(self) -> ResolvedAssignmentQuery:
        """ Get a query representation of this assignment. """

        return ResolvedAssignmentQuery(self)
