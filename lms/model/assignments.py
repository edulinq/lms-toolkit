import typing

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
            id: typing.Union[str, None] = None,
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

        self.id: typing.Union[str, None] = id
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

class AssignmentQuery():
    """
    A class for the different ways one can attempt to reference an LMS assignment.
    In general, an assignment can be queried by:
     - LMS Assignment ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    def __init__(self,
            id: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
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

    def match(self, target: Assignment) -> bool:
        """ Check if this query matches an assignment. """

        for field_name in ['id', 'name']:
            self_value = getattr(self, field_name, None)
            target_value = getattr(target, field_name, None)

            if (self_value is None):
                continue

            if (self_value != target_value):
                return False

        return True

    def __str__(self) -> str:
        text = self.name

        if (self.id is not None):
            if (text is not None):
                text = f"{text} ({id})"
            else:
                text = self.id

        if (text is None):
            return '<unknown>'

        return text
