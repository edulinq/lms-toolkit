import os

import edq.testing.cli
import edq.testing.unittest

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
BASE_TESTDATA_DIR: str = os.path.join(THIS_DIR, "testdata")
TEST_CASES_DIR: str = os.path.join(BASE_TESTDATA_DIR, "tests")
DATA_DIR: str = os.path.join(BASE_TESTDATA_DIR, "data")

class CLITest(edq.testing.unittest.BaseTest):
    """ Test CLI invocations (without a backing server). """

    @classmethod
    def get_test_basename(cls, path: str) -> str:
        """ Get the test's name based off of its filename and location. """

        return edq.testing.cli.compute_ancestor_basename(path, TEST_CASES_DIR)

def disable_serverrunner_reset(
    test: edq.testing.unittest.BaseTest,
    test_info: edq.testing.cli.CLITestInfo,
    ) -> None:
    """
    A setup/teardown function for disabling server runner resets.
    """

    server_runner = getattr(test, 'server_runner', None)
    if (server_runner is None):
        return

    server_runner.skip_restart = True

def enable_serverrunner_reset(
    test: edq.testing.unittest.BaseTest,
    test_info: edq.testing.cli.CLITestInfo,
    ) -> None:
    """
    A setup/teardown function for enabling server runner resets.
    """

    server_runner = getattr(test, 'server_runner', None)
    if (server_runner is None):
        return

    server_runner.skip_restart = False
    server_runner.restart()

# Populate CLITest with all the test methods.
edq.testing.cli.discover_test_cases(CLITest, TEST_CASES_DIR, DATA_DIR)
