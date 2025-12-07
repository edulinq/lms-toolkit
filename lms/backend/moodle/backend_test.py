import os
import typing

import edq.testing.cli

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

MOODLE_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-moodle-testdata', 'testdata', 'http')

DEFAULT_USER: str = 'course-owner'

class MoodleBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Moodle. """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

        # Skip exchange verification tests, since Moodle users are not logged in ahead of time.
        # This makes the exchanges dependent on the login.
        self.skip_test_exchanges_base = True

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_MOODLE

        cls.backend_type = lms.model.constants.BACKEND_TYPE_MOODLE

        cls.exchanges_dir = MOODLE_TEST_EXCHANGES_DIR

        cls.backend_args.update({
            'auth_user': DEFAULT_USER,
            'auth_password': DEFAULT_USER,
        })

        cls.headers_to_skip += [
            'edq-lms-moodle-user',
        ]

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        super().modify_cli_test_info(test_info)

        test_info.arguments += [
            '--auth-user', self.backend._username,
            '--auth-password', self.backend._password,
        ]

    def set_user(self, email: str) -> None:
        super().set_user(email)

        username = email.split('@')[0]

        # Remember that test passwords are the same as usernames.
        self.backend._username = username
        self.backend._password = username

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(MoodleBackendTest)
