import typing

import lms.model.base
import lms.model.query
import lms.model.users

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
            group: 'Group',
            **kwargs: typing.Any) -> None:
        super().__init__(id = group.id, name = group.name, **kwargs)

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

    def to_query(self) -> ResolvedGroupQuery:
        """ Get a query representation of this group. """

        return ResolvedGroupQuery(self)

class GroupMembership(lms.model.base.BaseType):
    """
    An instance of a user being in a group.
    """

    CORE_FIELDS = [
        'group', 'user',
    ]

    def __init__(self,
            user: lms.model.users.UserQuery,
            group: GroupQuery,
            **kwargs: typing.Any) -> None:
        super().__init__(**kwargs)

        self.group: GroupQuery = group
        """ The group the user belongs to. """

        self.user: lms.model.users.UserQuery = user
        """ The user in a group. """

    def update_queries(self,
            users: typing.Union[typing.Dict[str, lms.model.users.ResolvedUserQuery], None] = None,
            groups: typing.Union[typing.Dict[str, ResolvedGroupQuery], None] = None,
            ) -> None:
        """
        Update the queries with resolved variants.
        The maps should be keyed by respective ids.
        """

        if ((users is not None) and (self.user.id in users)):
            self.user = users[self.user.id]

        if ((groups is not None) and (self.group.id in groups)):
            self.group = groups[self.group.id]
