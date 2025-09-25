import typing

import edq.util.json
import edq.util.time

class Assignment(edq.util.json.DictConverter):
    """
    An assignment within a course.
    """

    COMMON_FIELDS: list[str] = [
        'id', 'name', 'description',
        'open_date', 'close_date', 'due_date',
        'points_possible', 'position', 'group_id',
    ]
    """ The common fields shared across backends for this type. """

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

        self.extra_fields: typing.Dict[str, typing.Any] = kwargs.copy()
        """ Additional fields not common to all backends or explicitly used by the creating child backend. """

    def __eq__(self, other: object) -> bool:
        if (not isinstance(other, Assignment)):
            return False

        # Check the common fields only.
        for field_name in self.COMMON_FIELDS:
            if (getattr(self, field_name) != getattr(other, field_name)):
                return False

        return True
