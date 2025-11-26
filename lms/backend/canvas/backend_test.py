import os
import typing

import edq.testing.cli

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

CANVAS_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-canvas-testdata', 'testdata', 'http')

USER_TOKENS: typing.Dict[str, str] = {
    'course-admin@test.edulinq.org': 'nHRkQ39czXL2x7xxKrPYmvtYTyWJCCHCVRMZTfTfZtJZZWXHnkN9UhnCy37XuYeK',
    'course-grader@test.edulinq.org': 'uwRzuhDzDyEJBuJ8QR8PRTLAZHRU7ErY6aTtACNtB7tHZNVzLLw2AGZTGLQya9YX',
    'course-other@test.edulinq.org': 'VntnXWUfHDYDGhFV8VPmUrMEVuwJ3JeJ898FFDf7DHkGJ7vmrEW3eJx9cuHukh94',
    'course-owner@test.edulinq.org': 'xkC8V8BWX4RFx7JMYyZuyDvtDAKRxuGHRxTR268eHzXCPYU46vw89DrBADat4n6U',
    'course-student@test.edulinq.org': 'T7J3DQMJzamkcPVWtkRh6zczx7CHEBy3JGJkvEeavcQyVKDGL9MAkveyJyDuAUEL',
    'server-admin@test.edulinq.org': 'hHKUya4aDV6BnPDuDv8rL7TBFmxmGuBzTMFRrmFfDNaZM4Wy7WQKfufNt9kW9m3W',
    'server-creator@test.edulinq.org': 'R9Z9GhYLrUArnc2cTAeu3Q7fkBhw7CZtuKB8A9eTVhvHWFKWrDVD769GnNzraAGJ',
    'server-owner@test.edulinq.org': 'ycY4AhQ8ZGwk7L38vGur9HtG2WXevMcRh62eXU8KAfGRuXaXhXZE2wCthWVzRZn2',
    'server-user@test.edulinq.org': 'vYNF6mWfcz4mQYBG6XJXeJh8x4WNNeQHkEkVDWAQxc8JBC9GJFwCffP9fznK4QMK',
}
"""
The tokens for each known user.
These tokens were taken from the Canvas test data repo:
https://github.com/edulinq/lms-docker-canvas-testdata
"""

DEFAULT_TOKEN: str = USER_TOKENS['course-owner@test.edulinq.org']
""" The default token for these tests. """

class CanvasBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Canvas. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_CANVAS

        cls.backend_type = lms.model.constants.BACKEND_TYPE_CANVAS

        cls.exchanges_dir = CANVAS_TEST_EXCHANGES_DIR

        cls.backend_args.update({
            'auth_token': DEFAULT_TOKEN,
        })

        cls.params_to_skip += [
            'per_page',
        ]

        cls.headers_to_skip += [
        ]

    def modify_cli_test_info(self, test_info: edq.testing.cli.CLITestInfo) -> None:
        super().modify_cli_test_info(test_info)

        test_info.arguments += [
            '--auth-token', self.backend.auth_token,
        ]

    def set_user(self, email: str) -> None:
        super().set_user(email)

        # Update the token the backend is using.
        self.backend.auth_token = USER_TOKENS[email]

    def clear_user(self) -> None:
        super().clear_user()

        # Switch back to the default token.
        self.backend.auth_token = DEFAULT_TOKEN

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(CanvasBackendTest)
