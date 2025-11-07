import typing

import lms.backend.canvas.common
import lms.backend.canvas.model
import lms.model.groups

BASE_ENDPOINT = "/api/v1/group_categories/{groupset_id}/groups?per_page={page_size}"

def request(backend: typing.Any,
        course_id: int,
        groupset_id: int,
        ) -> typing.List[lms.model.groups.Group]:
    """ List a group set's groups. """

    url = backend.server + BASE_ENDPOINT.format(groupset_id = groupset_id, page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers = headers)
    if (raw_objects is None):
        identifiers = {
            'course_id': course_id,
            'groupset_id': groupset_id,
        }
        backend.not_found('list groups', identifiers)

        return []

    return [lms.backend.canvas.model.group(raw_object) for raw_object in raw_objects]
