import os

import lms.backend.testing
import lms.model.constants

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_DIR: str = os.path.join(THIS_DIR, '..', '..', '..')
TEST_EXCHANGES_DIR: str = os.path.join(ROOT_DIR, "testdata", "canvas")

TEST_TOKEN: str = 'CANVAS_TEST_TOKEN'

class CanvasBackendTest(lms.backend.testing.BackendTest):
    """ A backend test for Canvas. """

    @classmethod
    def child_class_setup(cls) -> None:
        cls.server_key = lms.model.constants.BACKEND_TYPE_CANVAS

        cls.backend_type = lms.model.constants.BACKEND_TYPE_CANVAS

        cls.exchanges_dir = TEST_EXCHANGES_DIR

        cls.backend_args.update({
            'token': TEST_TOKEN,
        })

        cls.params_to_skip += [
            'per_page',
        ]

        cls.headers_to_skip += [
            'Authorization',
        ]

# Attatch the backend tests to this class.
lms.backend.testing.discover_test_cases(CanvasBackendTest)
