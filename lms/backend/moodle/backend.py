# pylint: disable=abstract-method

import logging
import typing
import urllib.parse

import bs4
import edq.util.net

import lms.model.backend
import lms.model.constants
import lms.util.net

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

    def _login(self, update_server: bool = True) -> None:
        """
        Try to login to the Moodle server.
        If `update_server` is true, then this may try to update the backend's server location if redirected by the Moodle server.
        """

        # Check if we are already logged in.
        if (self._session_headers is not None):
            return

        response, body = edq.util.net.make_get(self.server + '/login/index.php')
        cookies = lms.util.net.parse_cookies(response.headers.get('set-cookie', None))

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
            'anchor': '',
            'logintoken': token,
            'username': self._username,
            'password': self._password,
        }

        response, _ = edq.util.net.make_post(self.server + '/login/index.php',
                headers = headers, data = data,
                allow_redirects = False)

        # Check for a successful login.
        cookies = lms.util.net.parse_cookies(response.headers.get('set-cookie', None))
        if ('moodleid1_' in cookies):
            self._session_headers = {
                'cookie': response.headers.get('set-cookie', None),
                # Insert a header to identify the user.
                'edq-lms-moodle-user': self._username,
            }
            return

        # Login Failed

        # The specified server/host needs to match exactly what the Moodle server wants it to be,
        # e.g., `127.0.0.1` does not work when the sevrer wants the host to be `localhost`.
        # If these do not match, we will get a redirect here.
        # Use this redirect to discover the correct server.
        location = response.headers.get('location', None)
        if (update_server and (location is not None) and (not location.startswith(self.server))):
            parts = urllib.parse.urlparse(location)
            host = f"{parts.scheme}://{parts.netloc}"

            logging.debug(("Mismatch in the client-specified server ('%s') and server-requested host ('%s')."
                    + " To avoid extra requests, update the server (e.g., `--server`) to match the host."),
                    self.server, host)

            # Update the server and try to login again (without updating the server again (to avoid loops)).
            self.server = host
            self._login(update_server = False)
            return

        raise ValueError(f"Could not log into Moodle server ({self.server}) with user '{self._username}'. Is username/password correct?")
