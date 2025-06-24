import lms.api.user.common
import lms.api.user.list
import lms.api.resolve

def fetch_and_resolve_users(server, token, course, user_queries,
        keys = lms.api.user.common.DEFAULT_KEYS, include_role = False,
        fill_missing = False):
    return lms.api.resolve.fetch_and_resolve(server, token, course, user_queries,
            lms.api.user.list.request, {'include_role': include_role},
            keys = keys, resolve_kwargs = {'fill_missing': fill_missing})

def requires_resolution(users):
    return lms.api.resolve.requires_resolution(users)
