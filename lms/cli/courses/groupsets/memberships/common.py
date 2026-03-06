import typing

import lms.model.backend
import lms.model.groups
import lms.util.tsv

def load_group_memberships(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: bool,
        ) -> typing.List[lms.model.groups.GroupMembership]:
    """ Read a group membership TSV file. """

    memberships: typing.List[lms.model.groups.GroupMembership] = []
    for row in lms.util.tsv.read_tsv(path, ['group', 'user'], skip_rows):
        lineno = row['__lineno__']
        if not row.get('__has_header__'):
            parts_len = len(row.get('__parts__', []))
            if parts_len != 2:
                raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values. Expecting 2, found {parts_len}.")
        group_query = backend.parse_group_query(row['group'])
        if (group_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a group query that could not be parsed: '{row['group']}'.")
        user_query = backend.parse_user_query(row['user'])
        if (user_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a user query that could not be parsed: '{row['user']}'.")
        memberships.append(lms.model.groups.GroupMembership(group = group_query, user = user_query))
    return memberships
