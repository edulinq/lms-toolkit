import typing

import lms.backend.canvas.common
import lms.model.assignments
import lms.model.scores
import lms.model.users
import lms.util.parse

CORE_FIELDS: typing.List[str] = [
    'id',
    'assignment_id',
    'user_id',
]

class AssignmentScore(lms.model.scores.AssignmentScore):
    """
    A Canvas assignment score.

    Common fields will be held in lms.model.scores.AssignmentScore.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.base.BaseType.extra_fields.

    See: https://developerdocs.instructure.com/services/canvas/resources/scores
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas assignment score is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = lms.util.parse.required_string(kwargs.get('id', None), 'id')
        kwargs['score'] = lms.util.parse.optional_float(kwargs.get('score', None), 'score')
        kwargs['points_possible'] = lms.util.parse.optional_float(kwargs.get('points_possible', None), 'points_possible')
        kwargs['submission_date'] = lms.backend.canvas.common.parse_timestamp(kwargs.get('submitted_at', None))
        kwargs['graded_date'] = lms.backend.canvas.common.parse_timestamp(kwargs.get('graded_at', None))

        assignment_id = lms.util.parse.required_string(kwargs.get('assignment_id', None), 'assignment_id')
        kwargs['assignment_query'] = lms.model.assignments.AssignmentQuery(id = assignment_id)

        user_id = lms.util.parse.required_string(kwargs.get('user_id', None), 'user_id')
        kwargs['user_query'] = lms.model.users.UserQuery(id = user_id)

        super().__init__(**kwargs)
