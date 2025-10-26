import typing

import lms.model.base
import lms.model.query

class Group(lms.model.base.BaseType):
    """
    A formal collection of users.
    """

    CORE_FIELDS = [
        'id', 'name',
    ]

    def __init__(self,
            id: typing.Union[str, int, None] = None,
            name: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        if (id is None):
            raise ValueError("Groups must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this group. """

        self.name: typing.Union[str, None] = name
        """ The display name of this group. """

    def to_query(self) -> 'GroupQuery':
        """ Get a query representation of this group. """

        return GroupQuery(id = self.id, name = self.name)

class GroupQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS group.
    In general, a group can be queried by:
     - LMS Group ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedGroupQuery(lms.model.query.ResolvedBaseQuery, GroupQuery):
    """
    A GroupQuery that has been resolved (verified) from a real group instance.
    """

    _include_email = False

    def __init__(self,
            group: Group,
            **kwargs: typing.Any) -> None:
        super().__init__(id = group.id, name = group.name, **kwargs)
