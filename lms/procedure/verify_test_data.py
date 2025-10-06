"""
Supporting code for verifying test data.
See `lms.procedure.server` for the inputs (parser) to this procedure.
"""

import argparse
import typing

import edq.procedure.verify_exchanges

import lms.procedure.server

def run(args: typing.Union[argparse.Namespace, typing.Dict[str, typing.Any]]) -> int:
    """
    Run the procedure.
    The arguments may come directly from the parser for lms.cli.lib.verify-test-data.
    """

    if (not isinstance(args, dict)):
        args = vars(args)

    args.update(args.get('_config', {}))

    test_data_dir = args.get('test_data_dir', None)
    if (test_data_dir is None):
        raise ValueError("No test data dir was providded.")

    server_runner = lms.procedure.server.ServerRunner(**args)
    server_runner.start()

    failure_count = int(edq.procedure.verify_exchanges.run([test_data_dir], server_runner.server))

    server_runner.stop()

    return failure_count
