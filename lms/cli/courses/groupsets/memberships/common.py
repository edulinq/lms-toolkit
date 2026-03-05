import typing
import lms.cli.table
import lms.model.backend
import lms.model.groups

def load_group_memberships(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: bool,
        ) -> typing.List[lms.model.groups.GroupMembership]:
    """ Read a group membership TSV file. """

    memberships: typing.List[lms.model.groups.GroupMembership] = []

    rows = lms.cli.table.read_table(path, ['group', 'user'], skip_rows)
    for (lineno, row) in rows:
        group_query = backend.parse_group_query(row['group'])
        if (group_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a group query that could not be parsed: '{row['group']}'.")

        user_query = backend.parse_user_query(row['user'])
        if (user_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a user query that could not be parsed: '{row['user']}'.")

        memberships.append(lms.model.groups.GroupMembership(group = group_query, user = user_query))

    return memberships
