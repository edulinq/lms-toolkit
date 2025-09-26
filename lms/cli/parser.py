"""
Customize an argument parser for LMS Toolkit.
"""

import edq.core.argparser

import lms.model.constants

def get_parser(description: str,
        include_output_format: bool = False,
        include_course: bool = False,
        ) -> edq.core.argparser.Parser:
    """
    Get an argument parser specialized for LMS Toolkit.
    """

    # TEST - Set a filename for the config search. "edq-lms.json"?

    parser = edq.core.argparser.get_default_parser(description)

    if (include_output_format):
        parser.add_argument('--format', dest = 'output_format',
            action = 'store', type = str,
            default = lms.model.constants.OUTPUT_FORMAT_TEXT, choices = lms.model.constants.OUTPUT_FORMATS,
            help = 'The format to display the outut as (default: %(default)s).')

        parser.add_argument('--skip-headers', dest = 'skip_headers',
            action = 'store_true', default = False,
            help = 'Skip headers when outputting results, will not apply to all formats (default: %(default)s).')

    if (include_course):
        parser.add_argument('--course', dest = 'course',
            action = 'store', type = str, default = None,
            help = 'The course to target for this operation.')
