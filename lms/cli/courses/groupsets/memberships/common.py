import typing

import lms.cli.table
import lms.model.backend
import lms.model.groups

GROUP_MEMBERSHIP_COLUMNS: typing.List[lms.cli.table.ColumnDef] = [
    lms.cli.table.ColumnDef("group", required = True),
    lms.cli.table.ColumnDef("user", required = True),
]

def load_group_memberships(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: int,
        has_header: bool = False,
        ) -> typing.List[lms.model.groups.GroupMembership]:
    """ Read a group membership TSV file. """

    rows = lms.cli.table.read_table(path, GROUP_MEMBERSHIP_COLUMNS,
            skip_rows = skip_rows, has_header = has_header)

    memberships: typing.List[lms.model.groups.GroupMembership] = []

    for (lineno, values) in rows:
        group_raw = values[0]
        user_raw = values[1]

        group_query = backend.parse_group_query(typing.cast(str, group_raw))
        if (group_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a group query that could not be parsed: '{group_raw}'.")

        user_query = backend.parse_user_query(typing.cast(str, user_raw))
        if (user_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a user query that could not be parsed: '{user_raw}'.")

        memberships.append(lms.model.groups.GroupMembership(group = group_query, user = user_query))

    return memberships
