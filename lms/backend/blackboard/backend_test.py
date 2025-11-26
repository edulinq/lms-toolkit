import os

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

BLACKBOARD_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-blackboard-testdata', 'testdata', 'http')

class BlackboardBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Blackboard. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_BLACKBOARD

        cls.backend_type = lms.model.constants.BACKEND_TYPE_BLACKBOARD

        cls.exchanges_dir = BLACKBOARD_TEST_EXCHANGES_DIR

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(BlackboardBackendTest)
