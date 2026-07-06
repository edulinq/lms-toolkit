import os

import edq.net.request
import edq.net.settings
import edq.testing.cli

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

BLACKBOARD_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-blackboard-testdata', 'testdata', 'http')

DEFAULT_USER: str = 'course-owner'

class BlackboardBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Blackboard. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BackendType.BLACKBOARD.value

        cls.backend_type = lms.model.constants.BackendType.BLACKBOARD

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

        edq.net.settings.set_https_verification(False)

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        super().modify_cli_test_info(test_info)

        if (test_info.extra_options.get('skip_auth', False) is not True):
            test_info.arguments += [
                '--auth-user', self.backend.auth_user,
                '--auth-password', self.backend.auth_password,
            ]

    def set_user(self, email: str) -> None:
        super().set_user(email)

        username = email.split('@')[0]

        # Remember that test passwords are the same as usernames.
        self.backend.auth_user = username
        self.backend.auth_password = username

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(BlackboardBackendTest)
