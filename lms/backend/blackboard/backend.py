# pylint: disable=abstract-method

import typing

import edq.util.net

import lms.backend.blackboard.model
import lms.model.backend
import lms.model.constants
import lms.model.courses
import lms.model.users
import lms.util.net
import lms.util.parse

class BlackboardBackend(lms.model.backend.APIBackend):
    """ An API backend for the Blackboard Learn LMS. """

    def __init__(self,
            server: str,
            auth_user: typing.Union[str, None] = None,
            auth_password: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(server, lms.model.constants.BACKEND_TYPE_BLACKBOARD, **kwargs)

        if (auth_user is None):
            raise ValueError("Blackboard backends require a username.")

        if (auth_password is None):
            raise ValueError("Blackboard backends require a password.")

        self._username = auth_user
        """ The username to authenticate with. """

        self._password = auth_password
        """ The password to authenticate with. """

        self._session_headers: typing.Union[typing.Dict[str, typing.Any], None] = None
        """ The headers (e.g., cookies) for our logged in Blackboard session. """

    def _login(self) -> None:
        """ Try to login to the Blackboard server. """

        # Check if we are already logged in.
        if (self._session_headers is not None):
            return

        response, _ = edq.util.net.make_get(self.server)
        cookies, router_params = self._parse_bb_cookies(response.headers.get('set-cookie', None))

        new_cookies = {
            'BbRouter': cookies['bbrouter']
        }

        text_cookies = '; '.join(['='.join(items) for items in new_cookies.items()])

        headers = {
            'cookie': text_cookies,
        }
        data = {
            'user_id': self._username,
            'password': self._password,
            'blackboard.platform.security.NonceUtil.nonce.ajax': router_params['xsrf'],
        }

        response, _ = edq.util.net.make_post(self.server + '/webapps/login/',
                headers = headers, data = data,
                # Don't store the nonce in exchanges.
                params_to_skip = ['blackboard.platform.security.NonceUtil.nonce.ajax'],
                allow_redirects = False)

        cookies, router_params = self._parse_bb_cookies(response.headers.get('set-cookie', None))
        if ('sessionId' not in router_params):
            raise ValueError(f"Could not log into Blackboard server ({self.server}) with user '{self._username}'. Is username/password correct?")

        self._session_headers = {
            'cookie': response.headers.get('set-cookie', None),
            'x-blackboard-xsrf': router_params['xsrf'],
            # Insert a header to identify the user.
            'edq-lms-blackboard-user': self._username,
        }

    def _parse_bb_cookies(self, text_cookies: typing.Union[str, None]) -> typing.Tuple[typing.Dict[str, typing.Any], typing.Dict[str, str]]:
        """
        Parse out the Blackboard cookies and return two dicts:
         - All cookies (with lower case keys).
         - The router params/cookies (specific to Blackboard).
        """

        cookies: typing.Dict[str, typing.Any] = {}
        router_params: typing.Dict[str, str] = {}

        # If we are testing, return fake cookies.
        if (self.is_testing()):
            cookies['bbrouter'] = 'xsrf:abc,sessionId:9999999'
            router_params['xsrf'] = 'abc'
            router_params['sessionId'] = '9999999'

            return cookies, router_params

        cookies = lms.util.net.parse_cookies(text_cookies)

        router_text = cookies.get('bbrouter', None)
        if (isinstance(router_text, str)):
            for text in router_text.split(','):
                key, value = text.split(':', maxsplit = 1)
                router_params[key] = value

        return cookies, router_params

    def courses_list(self,
            **kwargs: typing.Any) -> typing.List[lms.model.courses.Course]:
        self._login()

        url = self.server + '/learn/api/public/v3/courses'
        data = {
            'availability.available': 'Yes',
        }
        response, _ = edq.util.net.make_get(url, headers = self._session_headers, data = data)

        courses = []
        for raw_course in response.json().get('results', []):
            courses.append(lms.backend.blackboard.model.course(raw_course))

        courses.sort()

        return courses

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        parsed_course_id = lms.util.parse.required_int(course_id, 'course_id')

        self._login()

        url = self.server + '/learn/api/public/v1/courses/{course_id}/users'
        url = url.format(course_id = lms.backend.blackboard.model.format_id(parsed_course_id))

        data = {
            'expand': 'user',
        }

        response, _ = edq.util.net.make_get(url, headers = self._session_headers, data = data)

        users = []
        for raw_user in response.json().get('results', []):
            users.append(lms.backend.blackboard.model.course_user(raw_user))

        users.sort()

        return users
