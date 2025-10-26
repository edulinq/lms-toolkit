import typing

import lms.model.groupsets
import lms.util.parse

CORE_FIELDS: typing.List[str] = [
    'id',
]

class GroupSet(lms.model.groupsets.GroupSet):
    """
    A Canvas group set associated with a course.

    Common fields will be held in lms.model.groups.GroupSet.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.groups.GroupSet.extra_fields.

    See: https://developerdocs.instructure.com/services/canvas/resources/group_categories
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas group set is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = lms.util.parse.required_string(kwargs.get('id', None), 'id')

        super().__init__(**kwargs)
