import typing

import edq.util.json
import edq.util.time

import lms.model.base

class Assignment(lms.model.base.BaseType):
    """
    An assignment within a course.
    """

    CORE_FIELDS = [
        'id', 'name', 'description',
        'open_date', 'close_date', 'due_date',
        'points_possible', 'position', 'group_id',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            description: typing.Union[str, None] = None,
            open_date: typing.Union[edq.util.time.Timestamp, None] = None,
            close_date: typing.Union[edq.util.time.Timestamp, None] = None,
            due_date: typing.Union[edq.util.time.Timestamp, None] = None,
            points_possible: typing.Union[float, None] = None,
            position: typing.Union[int, None] = None,
            group_id: typing.Union[str, None] = None,
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

        self.position: typing.Union[int, None] = position
        """ The order that this assignment should appear relative to other assignments. """

        self.group_id: typing.Union[str, None] = group_id
        """ The LMS's identifier for the group this assignment appears in. """

    def to_query(self) -> 'AssignmentQuery':
        """ Get a query representation of this user. """

        return AssignmentQuery(id = self.id, name = self.name)

class AssignmentQuery(edq.util.json.DictConverter):
    """
    A class for the different ways one can attempt to reference an LMS assignment.
    In general, an assignment can be queried by:
     - LMS Assignment ID (`id`)
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
            raise ValueError("Assignment query is empty, it must have at least one piece of information (id, name).")

    def requires_resolution(self) -> bool:
        """
        Check if this query needs to be resolved.
        Typically, this means that the query is not just an LMS ID.
        """

        return ((self.id is None) or (self.name is not None))

    def match(self, target: typing.Union[Assignment, 'AssignmentQuery', None]) -> bool:
        """ Check if this query matches an assignment. """

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
        if (not isinstance(other, AssignmentQuery)):
            return False

        return ((self.id, self.name) == (other.id, other.name))

    def __lt__(self, other: object) -> bool:
        if (not isinstance(other, AssignmentQuery)):
            return False

        return ((self.id, self.name) < (other.id, other.name))

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

class ResolvedAssignmentQuery(AssignmentQuery):
    """
    A AssignmentQuery that has been resolved (verified) from a real assignment instance.
    """

    def __init__(self,
            assignment: Assignment,
            **kwargs: typing.Any) -> None:
        super().__init__(id = assignment.id, name = assignment.name, **kwargs)

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

    def get_id(self) -> str:
        """ Get the ID (which must exists) for this query. """

        if (self.id is None):
            raise ValueError("A resolved query cannot be created without an ID.")

        return self.id
