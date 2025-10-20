import os

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')

MOODLE_TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, 'testdata', 'lms-docker-moodle-testdata', 'testdata', 'http')

class MoodleBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Moodle. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_MOODLE

        cls.backend_type = lms.model.constants.BACKEND_TYPE_MOODLE

        cls.exchanges_dir = MOODLE_TEST_EXCHANGES_DIR

# Attatch tests to this class.
lms.backend.testing.attach_test_cases(MoodleBackendTest)
