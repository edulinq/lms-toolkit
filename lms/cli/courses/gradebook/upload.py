"""
Upload a gradebook (as a table).
"""

import argparse
import ast
import sys

import edq.util.dirent

import lms.backend.instance
import lms.cli.common
import lms.cli.parser
import lms.model.backend
import lms.model.scores

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend = lms.backend.instance.get_backend(**config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    gradebook = _load_gradebook(backend, args.path)

    count = backend.courses_gradebook_resolve_and_upload(course_query, gradebook)

    print(f"Uploaded {count} Scores")

    return 0

def _load_gradebook(
        backend: lms.model.backend.APIBackend,
        path: str,
        ) -> lms.model.scores.Gradebook:
    assignments = []
    users = []
    scores = []

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        for line in file:
            if (line.strip() == ''):
                continue

            lineno += 1

            parts = [part.strip() for part in line.split("\t")]

            # Process the assignment queries.
            if (lineno == 1):
                if (len(parts) < 2):
                    raise ValueError(f"File '{path}' line {lineno} (assignments line) has the incorrect number of values."
                            + f" Need at least 2 values (user and single assignment), found {len(parts)}.")

                # Skip the users column.
                parts = parts[1:]

                for part in parts:
                    assignment = backend.parse_assignment_query(part)
                    if (assignment is None):
                        raise ValueError(f"File '{path}' line {lineno} has an assignment query that could not be parsed: '{part}'.")

                    assignments.append(assignment)

                continue

            if (len(parts) != (1 + len(assignments))):
                raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values."
                        + f" Expecting {1 + len(assignments)}, found {len(parts)}.")

            # Process user row.
            user = backend.parse_user_query(parts[0])
            if (user is None):
                raise ValueError(f"File '{path}' line {lineno} has an user query that could not be parsed: '{parts[0]}'.")

            users.append(user)

            # User part already processed.
            parts = parts[1:]

            for (i, part) in enumerate(parts):
                part = part.strip()
                if (len(part) == 0):
                    continue

                try:
                    float_score = float(ast.literal_eval(part))
                except Exception:
                    raise ValueError(f"File '{path}' line {lineno} has a score that cannot be converted to a number: '{part}'.")  # pylint: disable=raise-missing-from

                assignment_score = lms.model.scores.AssignmentScore(score = float_score, assignment_query = assignments[i], user_query = user)
                scores.append(assignment_score)

    gradebook = lms.model.scores.Gradebook(assignments, users)

    for score in scores:
        gradebook.add(score)

    return gradebook

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
    )

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each row has 2-3 columns: user query, score, and comment (optional).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
