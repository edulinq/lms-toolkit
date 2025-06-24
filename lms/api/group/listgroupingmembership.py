import csv
import logging

import lms.api.common
import lms.api.group.common
import lms.api.group.resolve

BASE_ENDPOINT = "/api/v1/group_categories/{grouping}/export"

# [(old name, new name), ...]
KEYS = [
    ('canvas_group_id', 'lms_group_id'),
    ('group_name', 'group_name'),
    ('login_id', 'email'),
]

def request(server = None, token = None, course = None,
        grouping = None, **kwargs):
    server = lms.api.common.validate_param(server, 'server')
    token = lms.api.common.validate_param(token, 'token')
    course = lms.api.common.validate_param(course, 'course', param_type = int)
    grouping = lms.api.common.validate_param(grouping, 'grouping')

    logging.info("Fetching course ('%s') groups for grouping '%s' from '%s'." % (str(course), str(grouping), server))

    if (lms.api.group.resolve.requires_resolution([grouping])):
        grouping = lms.api.group.resolve.fetch_and_resolve_grouping_id(server, token, course, grouping)

    if (grouping is None):
        return []

    url = server + BASE_ENDPOINT.format(grouping = grouping)
    headers = lms.api.common.standard_headers(token)

    _, _, content = lms.api.common.make_get_request(url, headers, fetch_next_url = False, json_body = False)

    items = []
    for row in csv.DictReader(content.strip().splitlines()):
        items.append({new_key: row.get(old_key, None) for (old_key, new_key) in KEYS})

    return items
