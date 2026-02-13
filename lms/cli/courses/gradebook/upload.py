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

    gradebook = _load_gradebook(backend, args.path, args.skip_rows, args.has_header)

    count = backend.courses_gradebook_resolve_and_upload(course_query, gradebook)

    print(f"Uploaded {count} Scores")

    return 0

def _load_gradebook(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: int = 0,
        has_header: bool = False,
        ) -> lms.model.scores.Gradebook:
    if (has_header and (skip_rows > 0)):
        raise ValueError("Cannot use both --header and --skip-rows.")

    assignments = []
    users = []
    scores = []

    # user_col: index of the user column in data rows (default: 0 for positional mode).
    # col_to_assign_idx: maps each data column index to its index in the assignments list.
    user_col = 0
    col_to_assign_idx = {}

    with open(path, 'r', encoding = edq.util.dirent.DEFAULT_ENCODING) as file:
        lineno = 0
        real_rows = 0
        header_parsed = False

        for line in file:
            if (line.strip() == ''):
                continue

            lineno += 1
            real_rows += 1

            parts = [part.strip() for part in line.split("\t")]

            # Skip rows (non-header mode).
            if ((not has_header) and (real_rows <= skip_rows)):
                continue

            # Parse the assignment header row.
            if (not header_parsed):
                header_parsed = True

                if (has_header):
                    # Named header: locate the "user" column (case-insensitive) and
                    # parse each remaining column as an assignment query.
                    # Columns that cannot be parsed as assignments are ignored as extra.
                    user_col = None
                    for (i, part) in enumerate(parts):
                        if (part.lower() == 'user'):
                            if (user_col is not None):
                                raise ValueError(f"File '{path}' line {lineno} has a duplicate 'user' column.")
                            user_col = i
                        else:
                            assignment = backend.parse_assignment_query(part)
                            if (assignment is not None):
                                col_to_assign_idx[i] = len(assignments)
                                assignments.append(assignment)

                    if (user_col is None):
                        raise ValueError(f"File '{path}' line {lineno} is missing a required 'user' column.")

                else:
                    # Positional header: user is always at column 0, assignments follow.
                    if (len(parts) < 2):
                        raise ValueError(f"File '{path}' line {lineno} (assignments line) has the incorrect number of values."
                                + f" Need at least 2 values (user and single assignment), found {len(parts)}.")

                    user_col = 0
                    for (i, part) in enumerate(parts[1:], start = 1):
                        assignment = backend.parse_assignment_query(part)
                        if (assignment is None):
                            raise ValueError(f"File '{path}' line {lineno} has an assignment query that could not be parsed: '{part}'.")
                        col_to_assign_idx[i] = len(assignments)
                        assignments.append(assignment)

                continue

            # In positional mode, enforce exact column count on each data row.
            if (not has_header):
                expected = 1 + len(assignments)
                if (len(parts) != expected):
                    raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values."
                            + f" Expecting {expected}, found {len(parts)}.")

            # Process user column.
            if (user_col >= len(parts)):
                raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values.")

            user_raw = parts[user_col]
            user = backend.parse_user_query(user_raw)
            if (user is None):
                raise ValueError(f"File '{path}' line {lineno} has an user query that could not be parsed: '{user_raw}'.")

            users.append(user)

            # Process score columns.
            for (col_idx, assign_idx) in col_to_assign_idx.items():
                if (col_idx >= len(parts)):
                    continue

                part = parts[col_idx].strip()
                if (len(part) == 0):
                    continue

                try:
                    float_score = float(ast.literal_eval(part))
                except Exception:
                    raise ValueError(f"File '{path}' line {lineno} has a score that cannot be converted to a number: '{part}'.")  # pylint: disable=raise-missing-from

                assignment_score = lms.model.scores.AssignmentScore(score = float_score, assignment = assignments[assign_idx], user = user)
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
            include_skip_rows = True,
            include_header = True,
    )

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where the first row contains assignment queries and subsequent rows contain user queries and scores.')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
