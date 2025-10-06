"""
Supporting code for generating test data.
See `lms.procedure.server` for the inputs (parser) to this procedure.
"""

import argparse
import os
import typing

import edq.testing.run

import lms.backend.testing
import lms.procedure.server

THIS_DIR: str = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
ROOT_PACKAGE_DIR: str = os.path.join(THIS_DIR, '..')

def run(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Run the procedure.
    The arguments may come directly from the parser for lms.cli.lib.generate-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    server_runner = lms.procedure.server.ServerRunner(**args)
    server_runner.start()

    # Configure backend tests.
    lms.backend.testing.BackendTest.allowed_backend = server_runner.backend_type
    lms.backend.testing.BackendTest.skip_test_exchanges_base = True
    lms.backend.testing.BackendTest.override_server_url = server_runner.server

    # Run the tests (which generate the data).
    test_args = {
        'test_dirs': [ROOT_PACKAGE_DIR],
    }
    failure_count = int(edq.testing.run.run(test_args))

    server_runner.stop()

    return failure_count
