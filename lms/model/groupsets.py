import typing

import lms.model.base
import lms.model.query

class GroupSetQuery(lms.model.query.BaseQuery):
    """
    A class for the different ways one can attempt to reference an LMS group set.
    In general, a group set can be queried by:
     - LMS Group Set ID (`id`)
     - Full Name (`name`)
     - f"{name} ({id})"
    """

    _include_email = False

class ResolvedGroupSetQuery(lms.model.query.ResolvedBaseQuery, GroupSetQuery):
    """
    A GroupSetQuery that has been resolved (verified) from a real group set instance.
    """

    _include_email = False

    def __init__(self,
            group_set: 'GroupSet',
            **kwargs: typing.Any) -> None:
        super().__init__(id = group_set.id, name = group_set.name, **kwargs)

class GroupSet(lms.model.base.BaseType):
    """
    A collection of groups with a common purpose
    (e.g., a set of student groups for an assignment).
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
            raise ValueError("Group sets must have an id.")

        self.id: str = str(id)
        """ The LMS's identifier for this group set. """

        self.name: typing.Union[str, None] = name
        """ The display name of this group set. """

    def to_query(self) -> ResolvedGroupSetQuery:
        """ Get a query representation of this group set. """

        return ResolvedGroupSetQuery(self)
