import typing

import edq.util.dirent

import lms.model.backend
import lms.model.groups

def load_group_memberships(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: bool,
        ) -> typing.List[lms.model.groups.GroupMembership]:
    """ Read a group membership TSV file. """

    memberships: typing.List[lms.model.groups.GroupMembership] = []

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        real_rows = 0
        for line in file:
            lineno += 1

            if (line.strip() == ''):
                continue

            real_rows += 1

            if (real_rows <= skip_rows):
                continue

            parts = [part.strip() for part in line.split("\t")]
            if (len(parts) != 2):
                raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values. Expecting 2, found {len(parts)}.")

            group_query = backend.parse_group_query(parts[0])
            if (group_query is None):
                raise ValueError(f"File '{path}' line {lineno} has a group query that could not be parsed: '{parts[0]}'.")

            user_query = backend.parse_user_query(parts[1])
            if (user_query is None):
                raise ValueError(f"File '{path}' line {lineno} has a user query that could not be parsed: '{parts[1]}'.")

            memberships.append(lms.model.groups.GroupMembership(group = group_query, user = user_query))

    return memberships
