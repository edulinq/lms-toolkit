import typing

import edq.util.json
import edq.util.time

class Assignment(edq.util.json.DictConverter):
    """
    An assignment within a course.
    """

    def __init__(self,
            id: typing.Union[str, None] = None,
            name: typing.Union[str, None] = None,
            description: typing.Union[str, None] = None,
            available_date: typing.Union[edq.util.time.Timestamp, None] = None,
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

        self.available_date: typing.Union[edq.util.time.Timestamp, None] = available_date
        """ The datetime that this assignment becomes available at. """

        self.due_date: typing.Union[edq.util.time.Timestamp, None] = due_date
        """ The datetime that this assignment is due at. """

        self.points_possible: typing.Union[float, None] = points_possible
        """ The maximum number of points possible for this assignment. """

        self.position: typing.Union[int, None] = position
        """ The order that this assignment should appear relative to other assignments. """

        self.group_id: typing.Union[str, None] = group_id
        """ The LMS's identifier for the group this assignment appears in. """
