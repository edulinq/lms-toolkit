# pylint: disable=abstract-method

import json
import logging
import re
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

        self._edit_mode_enabled = False
        """ The session edit mode state. """

    def _enable_edit_mode(self, url: str) -> None:
        """
        Enable Moodle edit mode if not yet enabled.
        """

        response, _ = edq.net.request.make_get(url, headers = self._session_headers)

        sesskey_match = re.search(r'"sesskey":"([^"]+)"', response.text)
        if (sesskey_match):
            sesskey = sesskey_match.group(1)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        try:
            context = document.select_one('input[name=setmode]').get('data-context', None)  # type: ignore[union-attr]
        except AttributeError:
            _logger.warning("Unable to enable edit mode.")
            return

        params = {
            'sesskey': sesskey,
            'info': 'core_change_editmode',
        }

        data = [
            {
                'index': 0,
                'methodname': 'core_change_editmode',
                'args': {
                    'setmode': True,
                    'context': int(context),
                },
            }
        ]

        response, _ = edq.net.request.make_post(
            f"{self.server}/lib/ajax/service.php",
            additional_requests_options = {'params': params},
            data = json.dumps(data),
            headers = self._session_headers,
        )

        self._edit_mode_enabled = True

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
        self._login()

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
            except AttributeError:
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
        self._login()

        url = f"{self.server}/grade/report/grader/index.php?id={course_id}"

        self._enable_edit_mode(url)

        response, _ = edq.net.request.make_get(url, headers = self._session_headers)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        activities = document.select('table#user-grades th.item')

        assignments = []
        for activity in activities:
            # Parse and store the column's class (e.g. "c0").
            target_class = None
            column_classes = activity.get('class', None)
            column_class_pattern = re.compile(r'^c\d+$')
            for column_class in column_classes:
                if(column_class_pattern.match(column_class)):
                    target_class = column_class
                    break

            try:
                id = str(activity.get('data-itemid', None))
                name = str(activity.select_one('a.gradeitemheader').get_text())  # type: ignore[union-attr]
                points_possible = float(document.select_one(f'td.{target_class} input').get('max', None))
            except AttributeError:
                _logger.warning("Unable to retrieve assignment. Moodle data structure has changed. Contact project developers.")
                print("##############")
                print(target_class)
                print("##############")
                continue

            assignments.append(lms.model.assignments.Assignment(
                id = id,
                name = name,
                points_possible = points_possible,
            ))

        return assignments
