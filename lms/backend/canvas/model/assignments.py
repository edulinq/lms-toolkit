import typing

import lms.backend.canvas.common
import lms.model.assignments
import lms.util.parse

CORE_FIELDS: typing.List[str] = [
    'id',
]

class Assignment(lms.model.assignments.Assignment):
    """
    A Canvas assignment associated with a course.

    Common fields will be held in lms.model.assignments.Assignment.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.assignments.Assignment.extra_fields.

    See: https://developerdocs.instructure.com/services/canvas/resources/assignments
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas assignment is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = lms.util.parse.required_string(kwargs.get('id', None), 'id')
        kwargs['group_id'] = lms.util.parse.required_string(kwargs.get('assignment_group_id', None), 'id')
        kwargs['due_date'] = lms.backend.canvas.common.parse_timestamp(kwargs.get('due_at', None))
        kwargs['open_date'] = lms.backend.canvas.common.parse_timestamp(kwargs.get('unlock_at', None))
        kwargs['close_date'] = lms.backend.canvas.common.parse_timestamp(kwargs.get('lock_at', None))

        super().__init__(**kwargs)
