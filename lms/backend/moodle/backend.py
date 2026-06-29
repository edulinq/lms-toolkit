# pylint: disable=abstract-method

import logging
import typing
import urllib.parse

import bs4
import edq.net.request
import requests

import lms.model.backend
import lms.model.constants
import lms.util.net

_logger = logging.getLogger(__name__)

ROLE_MAPPING: typing.Dict[str, lms.model.users.CourseRole] = {
    "guest": lms.model.users.CourseRole.OTHER,
    "student": lms.model.users.CourseRole.STUDENT,
    "non-editing teacher": lms.model.users.CourseRole.GRADER,
    "teacher": lms.model.users.CourseRole.ADMIN,
    "manager": lms.model.users.CourseRole.OWNER,
}

# Moodle shows 5000 users per page when asked to fetch all results.
RESULTS_PER_PAGE: int = 5000

class MoodleBackend(lms.model.backend.APIBackend):
    """ An API backend for the Moodle LMS. """

    def __init__(self,
            server: str,
            auth_user: typing.Union[str, None] = None,
            auth_password: typing.Union[str, None] = None,
            **kwargs: typing.Any) -> None:
        super().__init__(server, lms.model.constants.BACKEND_TYPE_MOODLE, **kwargs)

        if (auth_user is None):
            raise ValueError("Moodle backends require a username.")

        if (auth_password is None):
            raise ValueError("Moodle backends require a password.")

        self._username = auth_user
        """ The username to authenticate with. """

        self._password = auth_password
        """ The password to authenticate with. """

        self._session_headers: typing.Union[typing.Dict[str, typing.Any], None] = None
        """ The headers (e.g., cookies) for our logged in Moodle session. """

    def _parse_cookies(self, response: requests.Response) -> typing.Dict[str, typing.Any]:
        """
        Parse Moodle cookies.
        Return fake cookies when testing.
        """

        if (self.is_testing()):
            return {
                'moodlesession': 'testing-moodle-session',
                'moodleid1_': 'testing-moodle-id',
            }

        return lms.util.net.parse_cookies(response.headers.get('set-cookie', None))

    def _login(self, update_server: bool = True) -> None:
        """
        Try to login to the Moodle server.
        If `update_server` is true, then this may try to update the backend's server location if redirected by the Moodle server.
        """

        # Check if we are already logged in.
        if (self._session_headers is not None):
            return

        response, body = edq.net.request.make_get(self.server + '/login/index.php')
        cookies = self._parse_cookies(response)

        new_cookies = {
            'MoodleSession': cookies['moodlesession'],
        }
        text_cookies = '; '.join(['='.join(items) for items in new_cookies.items()])

        # Parse the login token from the page HTML.
        document = bs4.BeautifulSoup(body, 'html.parser')
        token = document.select('input[name="logintoken"]')[0]['value']

        headers = {
            'cookie': text_cookies,
            'host': urllib.parse.urlparse(self.server).netloc,
        }

        data = {
            'logintoken': token,
            'username': self._username,
            'password': self._password,
        }

        response, _ = edq.net.request.make_post(self.server + '/login/index.php',
                headers = headers, data = data,
                allow_redirects = False)

        # Check for a successful login.
        cookies = self._parse_cookies(response)
        if ('moodleid1_' in cookies):
            self._session_headers = {
                'cookie': response.headers.get('set-cookie', None),
                # Insert a header to identify the user.
                'edq-lms-moodle-user': self._username,
            }
            return

        # Login Failed

        # The specified server/host needs to match exactly what the Moodle server wants it to be,
        # e.g., `127.0.0.1` does not work when the server wants the host to be `localhost`.
        # If these do not match, we will get a redirect here.
        # Use this redirect to discover the correct server.
        location = response.headers.get('location', None)
        if (update_server and (location is not None) and (not location.startswith(self.server))):
            parts = urllib.parse.urlparse(location)
            host = f"{parts.scheme}://{parts.netloc}"

            _logger.debug(("Mismatch in the client-specified server ('%s') and server-requested host ('%s')."
                    + " To avoid extra requests, update the server (e.g., `--server`) to match the host."),
                    self.server, host)

            # Update the server and try to login again (without updating the server again (to avoid loops)).
            self.server = host
            self._login(update_server = False)
            return

        raise ValueError(f"Could not log into Moodle server ({self.server}) with user '{self._username}'. Is username/password correct?")

    def courses_list(self,
            **kwargs: typing.Any) -> typing.List[lms.model.courses.Course]:
        self._login()

        url = self.server + "/user/profile.php"
        response, _ = edq.net.request.make_get(url, headers = self._session_headers)

        document = bs4.BeautifulSoup(response.text, 'html.parser')
        cards = document.select('div.card-body')

        node = None
        for card in cards:
            text = card.get_text()
            if (text.startswith("Course details")):
                node = card
                break

        if (node is None):
            return []

        links = node.select('a')

        courses = []
        for link in links:
            name = link.get_text()

            href = link.get('href', None)
            if (href is None):
                continue

            id = str(href).rsplit("=", maxsplit = 1)[-1]

            courses.append(lms.model.courses.Course(
                id = id,
                name = name,
            ))

        return sorted(courses)

    def courses_users_list(self,
            course_id: str,
            **kwargs: typing.Any) -> typing.List[lms.model.users.CourseUser]:
        url = f"{self.server}/user/index.php?id={course_id}&perpage={RESULTS_PER_PAGE}"
        response, _ = edq.net.request.make_get(url, headers = self._session_headers)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        headers = document.select('table#participants thead tr th')
        # { course_user_attribute (e.g. name): column class, ... }
        classes = {}
        for header in headers:
            column_classes = header.get('class', None)
            if (column_classes is None):
                continue

            # Parse and store the column's class (e.g. "c0").
            # This class is referenced when storing corresponding course user data.
            if (isinstance(column_classes, str)):
                column_class = column_classes
            else:
                if ('header' in column_classes):
                    column_classes.remove('header')

                if (len(column_classes) != 1):
                    continue

                column_class = column_classes[0]

            elements = header.select('div.commands a')
            for element in elements:
                attribute = element.get('data-column', None)
                if (attribute is None):
                    continue

                classes[attribute] = column_class

        rows = document.select('table#participants tbody tr:not(.emptyrow)')

        users = []
        for row in rows:
            try:
                id = row.select_one('.cell input[type="checkbox"]').get('id', None).removeprefix('user')  # type: ignore[union-attr]
                name = row.select_one(f'.cell.{classes["fullname"]} a span').get('title', None).removeprefix('__EMPTY_NAME__ ')  # type: ignore[union-attr] # pylint: disable=line-too-long
                email = row.select_one(f'.cell.{classes["email"]}').get_text()  # type: ignore[union-attr]
                raw_role = row.select_one(f'.cell.{classes["roles"]} span a').get_text().strip().lower()  # type: ignore[union-attr]
            except AttributeError as _:
                _logger.warning("Unable to list users. Moodle data structure has changed. Contact project developers.")
                continue

            # HACK(JK): Moodle does not allow the Guest role when loading test data, so we patch the guest role during testing.
            if (email == 'course-other@test.edulinq.org'):
                raw_role = "guest"

            users.append(lms.model.users.CourseUser(
                id = id,
                name = name,
                email = email,
                raw_role = raw_role,
                role = ROLE_MAPPING.get(raw_role, None),
            ))

        return users

    def courses_assignments_list(self,
                course_id: str,
                **kwargs: typing.Any) -> typing.List[lms.model.assignments.Assignment]:
        url = f"{self.server}/course/view.php?id={course_id}"
        response, _ = edq.net.request.make_get(url, headers = self._session_headers)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        activities = document.select('ul li.activity')

        assignments = []
        for activity in activities:
            try:
                id = activity.get('data-id', None)
                name = activity.select_one('.activity-item').get('data-activityname', None)  # type: ignore[union-attr]
            except AttributeError as _:
                _logger.warning("Unable to retrieve assignment ID and/or name. Moodle data structure has changed. Contact project developers.")

            try:
                url = f"{self.server}/course/modedit.php?update={id}"
                response, _ = edq.net.request.make_get(url, headers = self._session_headers)  # type: ignore[misc]

                document = bs4.BeautifulSoup(response.text, 'html.parser')

                points_possible = document.select_one('input[name="grade[modgrade_point]"]').get('value', None)  # type: ignore[union-attr]
            except AttributeError as _:
                _logger.warning("Unable to retrieve assignment maximum point value. Moodle data structure has changed. Contact project developers.")

            assignments.append(lms.model.assignments.Assignment(
                id = str(id),
                name = str(name),
                points_possible = float(points_possible),  # type: ignore[arg-type]
            ))

        return assignments
