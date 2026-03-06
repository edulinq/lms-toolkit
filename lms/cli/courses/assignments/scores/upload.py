"""
Upload scores (and optional comments) for an assignment.
"""

import argparse
import ast
import sys
import typing

import lms.backend.instance
import lms.cli.common
import lms.cli.parser
import lms.model.backend
import lms.model.scores
import lms.model.users
import lms.util.tsv

def run_cli(args: argparse.Namespace) -> int:
    """ Run the CLI. """

    config = args._config

    backend = lms.backend.instance.get_backend(**config)

    course_query = lms.cli.common.check_required_course(backend, config)
    if (course_query is None):
        return 1

    assignment_query = lms.cli.common.check_required_assignment(backend, config)
    if (assignment_query is None):
        return 2

    scores = _load_scores(backend, args.path, args.skip_rows)

    count = backend.courses_assignments_scores_resolve_and_upload(course_query, assignment_query, scores)

    print(f"Uploaded {count} Scores")

    return lms.cli.common.strict_check(args.strict, (count != len(scores)),
        f"Expected to upload {len(scores)} scores, but uploaded {count}.", 3)

def _load_scores(
        backend: lms.model.backend.APIBackend,
        path: str,
        skip_rows: bool,
        ) -> typing.Dict[lms.model.users.UserQuery, lms.model.scores.ScoreFragment]:
    scores = {}
    for row in lms.util.tsv.read_tsv(path, ['user', 'score', 'comment'], skip_rows):
        lineno = row['__lineno__']
        if not row.get('__has_header__'):
            parts_len = len(row.get('__parts__', []))
            if parts_len not in [2, 3]:
                raise ValueError(f"File '{path}' line {lineno} has the incorrect number of values. Expecting 2-3, found {parts_len}.")
        user_query = backend.parse_user_query(row['user'])
        if (user_query is None):
            raise ValueError(f"File '{path}' line {lineno} has a user query that could not be parsed: '{row['user']}'.")
        score = None
        if (row['score'] != ''):
            try:
                score = float(ast.literal_eval(row['score']))
            except Exception:
                raise ValueError(f"File '{path}' line {lineno} has a score that cannot be converted to a number: '{row['score']}'.")  # pylint: disable=raise-missing-from
        comment = row['comment'] or None
        scores[user_query] = lms.model.scores.ScoreFragment(score = score, comment = comment)
    return scores

def main() -> int:
    """ Get a parser, parse the args, and call run. """
    return run_cli(_get_parser().parse_args())

def _get_parser() -> argparse.ArgumentParser:
    """ Get the parser. """

    parser = lms.cli.parser.get_parser(__doc__.strip(),
            include_course = True,
            include_assignment = True,
            include_skip_rows = True,
            include_strict = True,
    )

    parser.add_argument('path', metavar = 'PATH',
        action = 'store', type = str,
        help = 'Path to a TSV file where each row has 2-3 columns: user query, score, and comment (optional).')

    return parser

if (__name__ == '__main__'):
    sys.exit(main())
