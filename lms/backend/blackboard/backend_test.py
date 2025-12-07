import os
import typing

import edq.testing.cli
import edq.util.net

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

BLACKBOARD_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-blackboard-testdata', 'testdata', 'http')

DEFAULT_USER: str = 'course-owner'

class BlackboardBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Blackboard. """

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        super().__init__(*args, **kwargs)

        # Skip exchange verification tests, since Blackboard users are not logged in ahead of time.
        # This makes the exchanges dependent on the login.
        self.skip_test_exchanges_base = True

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_BLACKBOARD

        cls.backend_type = lms.model.constants.BACKEND_TYPE_BLACKBOARD

        cls.exchanges_dir = BLACKBOARD_TEST_EXCHANGES_DIR

        cls.backend_args.update({
            'auth_user': DEFAULT_USER,
            'auth_password': DEFAULT_USER,
        })

        cls.params_to_skip += [
            'blackboard.platform.security.NonceUtil.nonce.ajax',
        ]

        cls.headers_to_skip += [
            'edq-lms-blackboard-user',
            'x-blackboard-xsrf',
        ]

        edq.util.net._disable_https_verification()

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
lms.backend.testing.attach_test_cases(BlackboardBackendTest)
