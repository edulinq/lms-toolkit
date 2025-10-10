import typing

import edq.util.time

import lms.model.assignments
import lms.model.base
import lms.model.users

class AssignmentScore(lms.model.base.BaseType):
    """
    The score assignment to a student for an assignment (or scorable object).
    """

    CORE_FIELDS = [
        'id', 'score', 'points_possible', 'submission_date', 'graded_date', 'comment',
    ]

    def __init__(self,
            id: typing.Union[str, None] = None,
            score: typing.Union[float, None] = None,
            points_possible: typing.Union[float, None] = None,
            submission_date: typing.Union[edq.util.time.Timestamp, None] = None,
            graded_date: typing.Union[edq.util.time.Timestamp, None] = None,
            comment: typing.Union[str, None] = None,
            lms_assignment: typing.Union[lms.model.assignments.Assignment, None] = None,
            lms_user: typing.Union[lms.model.users.CourseUser, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this score. """

        self.score: typing.Union[float, None] = score
        """ The assignment score. """

        self.points_possible: typing.Union[float, None] = points_possible
        """ The maximum number of points possible for this assignment. """

        self.submission_date: typing.Union[edq.util.time.Timestamp, None] = submission_date
        """ The datetime that the submission that received this score was submitted. """

        self.graded_date: typing.Union[edq.util.time.Timestamp, None] = graded_date
        """ The datetime that the submission that received this score was graded. """

        self.comment: typing.Union[str, None] = comment
        """ A comment attached to this score. """

        self.lms_assignment: typing.Union[lms.model.assignments.Assignment, None] = lms_assignment
        """ The assignment associated with this score. """

        self.lms_user: typing.Union[lms.model.users.CourseUser, None] = lms_user
        """ The user associated with this score. """
