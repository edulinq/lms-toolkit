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
        'id', 'user_query', 'assignment_query', 'score', 'submission_date', 'graded_date', 'comment',
    ]

    def __init__(self,
            id: typing.Union[str, None] = None,
            score: typing.Union[float, None] = None,
            submission_date: typing.Union[edq.util.time.Timestamp, None] = None,
            graded_date: typing.Union[edq.util.time.Timestamp, None] = None,
            comment: typing.Union[str, None] = None,
            assignment_query: typing.Union[lms.model.assignments.AssignmentQuery, None] = None,
            user_query: typing.Union[lms.model.users.UserQuery, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.id: typing.Union[str, None] = id
        """ The LMS's identifier for this score. """

        self.assignment_query: typing.Union[lms.model.assignments.AssignmentQuery, None] = assignment_query
        """ The assignment associated with this score. """

        self.user_query: typing.Union[lms.model.users.UserQuery, None] = user_query
        """ The user associated with this score. """

        self.score: typing.Union[float, None] = score
        """ The assignment score. """

        self.submission_date: typing.Union[edq.util.time.Timestamp, None] = submission_date
        """ The datetime that the submission that received this score was submitted. """

        self.graded_date: typing.Union[edq.util.time.Timestamp, None] = graded_date
        """ The datetime that the submission that received this score was graded. """

        self.comment: typing.Union[str, None] = comment
        """ A comment attached to this score. """
