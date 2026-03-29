import typing

import lms.model.backend
import lms.model.groups
import lms.util.tsv

def load_group_memberships(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: int,
        ) -> typing.List[lms.model.groups.GroupMembership]:
    """ Read a group membership TSV file. """

    tsv = lms.util.tsv.load_tsv_table(
        path,
        ['group', 'user'],
        required_columns = ['group', 'user'],
        skip_rows = skip_rows,
    )

    memberships: typing.List[lms.model.groups.GroupMembership] = []

    if (tsv.header_map['group'] is None or tsv.header_map['user'] is None):
        raise ValueError(f"File '{path}' is missing required columns 'group' and/or 'user'.")

    max_required_index = max(tsv.header_map['group'], tsv.header_map['user'])

    for row in tsv.rows:
        if (tsv.headers is None):
            if (len(row.parts) != 2):
                row.raise_error(f"Has the incorrect number of values. Expecting 2, found {len(row.parts)}.")
        else:
            if (len(row.parts) <= max_required_index):
                row.raise_error(f"Has the incorrect number of values. Expecting 2, found {len(row.parts)}.")

        group_query = backend.parse_group_query(row.parts[tsv.header_map['group']])
        if (group_query is None):
            row.raise_error(f"Has a group query that could not be parsed: '{row.parts[tsv.header_map['group']]}'.")

        user_query = backend.parse_user_query(row.parts[tsv.header_map['user']])
        if (user_query is None):
            row.raise_error(f"Has a user query that could not be parsed: '{row.parts[tsv.header_map['user']]}'.")

        memberships.append(lms.model.groups.GroupMembership(group = group_query, user = user_query))

    return memberships
