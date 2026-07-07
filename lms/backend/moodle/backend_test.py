import os
import typing

import edq.testing.cli

import lms.backend.moodle.backend
import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

MOODLE_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-moodle-testdata', 'testdata', 'http')

DEFAULT_USER: str = 'course-owner'

class MoodleBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Moodle. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BackendType.MOODLE.value

        cls.backend_type = lms.model.constants.BackendType.MOODLE

        cls.exchanges_dir = MOODLE_TEST_EXCHANGES_DIR

        cls.backend_args.update({
            'auth_user': DEFAULT_USER,
            'auth_password': DEFAULT_USER,
        })

        cls.params_to_skip += [
            'logintoken',
        ]

        cls.headers_to_skip += [
            'edq-lms-moodle-user',
        ]

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        super().modify_cli_test_info(test_info)

        backend = typing.cast(lms.backend.moodle.backend.MoodleBackend, self.backend)

        if (test_info.extra_options.get('skip_auth', False) is not True):
            test_info.arguments += [
                '--auth-user', backend.auth_user,
                '--auth-password', backend.auth_password,
            ]

    def set_user(self, email: str) -> None:
        super().set_user(email)

        backend = typing.cast(lms.backend.moodle.backend.MoodleBackend, self.backend)

        username = email.split('@')[0]

        # Remember that test passwords are the same as usernames.
        backend.auth_user = username
        backend.auth_password = username

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(MoodleBackendTest)
