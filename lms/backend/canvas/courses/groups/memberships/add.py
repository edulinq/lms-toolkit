import os
import typing

import edq.util.dirent

import lms.backend.canvas.common
import lms.model.constants

BASE_ENDPOINT = "/api/v1/group_categories/{groupset_id}/import"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        group_id: int,
        user_ids: typing.List[int],
        ) -> int:
    """ Add users to a group. """

    url = backend.server + BASE_ENDPOINT.format(groupset_id = groupset_id)
    headers = backend.get_standard_headers()

    headers[lms.model.constants.HEADER_KEY_WRITE] = 'true'

    # Build a CSV.
    rows = ["canvas_user_id,canvas_group_id"]
    for user_id in sorted(user_ids):
        rows.append(f"{user_id},{group_id}")

    # Write CSV.
    temp_dir = edq.util.dirent.get_temp_dir('edq-lms-canvas-')
    temp_path = os.path.join(temp_dir, 'data.csv')
    edq.util.dirent.write_file_bytes(temp_path, "\n".join(rows).encode(edq.util.dirent.DEFAULT_ENCODING))

    files = {
        'attachment': open(temp_path, 'rb'),  # pylint: disable=consider-using-with
    }

    raw_object = lms.backend.canvas.common.make_post_request(url, headers = headers, files = files)
    if (raw_object is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
            'group_id': group_id,
            'user_ids': user_ids,
        }
        backend.not_found('add group memberships', identifiers)

        return 0

    return len(user_ids)
