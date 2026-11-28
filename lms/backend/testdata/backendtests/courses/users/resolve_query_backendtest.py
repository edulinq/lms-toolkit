import typing

import lms.backend.testing
import lms.model.testdata.users
import lms.model.users

def test_courses_users_resolve_query_base(test: lms.backend.testing.BackendTest) -> None:
    """ Resolve one user, preserve resolved queries, and reject missing users. """

    user = lms.model.testdata.users.COURSE_USERS['Course 101']['course-student'].to_query()
    test_cases: typing.List[typing.Tuple[typing.Dict[str, typing.Any], typing.Any, typing.Union[str, None]]] = [
        ({'course_id': '110000000', 'query': lms.model.users.UserQuery(name = 'course-student')}, user, None),
        ({'course_id': '110000000', 'query': user}, user, None),
        ({'course_id': '110000000', 'query': lms.model.users.UserQuery(id = '999')}, None, 'Could not resolve user query:'),
    ]

    test.base_request_test(test.get_backend().resolve_user_query, test_cases)
