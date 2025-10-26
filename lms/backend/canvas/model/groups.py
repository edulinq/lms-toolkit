import typing

import lms.model.groups
import lms.util.parse

CORE_FIELDS: typing.List[str] = [
    'id',
]

class Group(lms.model.groups.Group):
    """
    A Canvas group associated with a course.

    Common fields will be held in lms.model.groups.Group.
    Fields that are not common, but used by this backend will be explicitly listed.
    Other fields coming from Canvas will be held in lms.model.groups.Group.extra_fields.

    See: https://developerdocs.instructure.com/services/canvas/resources/groups
    """

    def __init__(self,
            **kwargs: typing.Any) -> None:
        # Check for important fields.
        for field in CORE_FIELDS:
            if (field not in kwargs):
                raise ValueError(f"Canvas group is missing '{field}'.")

        # Modify specific arguments before sending them to super.
        kwargs['id'] = lms.util.parse.required_string(kwargs.get('id', None), 'id')

        super().__init__(**kwargs)
