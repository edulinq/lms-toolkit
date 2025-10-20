import typing

import lms.backend.canvas.common
import lms.backend.canvas.model.courses

BASE_ENDPOINT = "/api/v1/courses?per_page={page_size}"

def request(backend: typing.Any,
        ) -> typing.List[lms.backend.canvas.model.courses.Course]:
    """ List courses. """

    url = backend.server + BASE_ENDPOINT.format(page_size = lms.backend.canvas.common.DEFAULT_PAGE_SIZE)
    headers = backend.get_standard_headers()

    raw_objects = lms.backend.canvas.common.make_get_request_list(url, headers)
    if (raw_objects is None):
        backend.not_found('course', {})

        return []

    return [lms.backend.canvas.model.courses.Course(**raw_object) for raw_object in raw_objects]
