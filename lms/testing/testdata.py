import argparse
import os
import typing

import edq.procedure.verify_exchanges
import edq.testing.run

import lms.backend.testing
import lms.backend.canvas.model
import lms.model.backend
import lms.testing.serverrunner

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_PACKAGE_DIR: str = os.path.join(THIS_DIR, '..')

def generate(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Generate HTTP test data by
    setting an exchange path, pointing to a live LMS server, and running all tests.
    The arguments may come directly from the parser for lms.cli.lib.generate-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    server_runner = lms.testing.serverrunner.LMSServerRunner(**args)
    server_runner.start()

    # Configure backend tests.
    lms.backend.testing.BackendTest.allowed_backend = server_runner.backend_type
    lms.backend.testing.BackendTest.skip_test_exchanges_base = True
    lms.backend.testing.BackendTest.override_server_url = server_runner.server
    lms.model.backend.APIBackend._testing_override = False
    lms.backend.canvas.model._testing_override = True

    # Run the tests (which generate the data).
    test_args = {
        'test_dirs': [ROOT_PACKAGE_DIR],
        'fail_fast': args.get('fail_fast', False),
    }
    failure_count = int(edq.testing.run.run(test_args))

    server_runner.stop()

    return failure_count

def verify(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Verify that test data matches data returned by the LMS server.
    The arguments may come directly from the parser for lms.cli.lib.verify-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    test_data_dir = args.get('test_data_dir', None)
    if (test_data_dir is None):
        raise ValueError("No test data dir was providded.")

    server_runner = lms.testing.serverrunner.LMSServerRunner(**args)
    server_runner.start()

    failure_count = int(edq.procedure.verify_exchanges.run([test_data_dir], server_runner.server, fail_fast = args.get('fail_fast', False)))

    server_runner.stop()

    return failure_count
