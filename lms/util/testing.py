import re
import typing

import edq.testing.asserts
import edq.testing.unittest

ID_SUBS: typing.List[typing.Tuple[re.Pattern, str]] = [
    (re.compile(r'^id: \d+'), 'id: <ID>'),  # Text
    (re.compile(r'^\d+\t'), "<ID>\t"),  # Table
    (re.compile(r'"id": "\d+"'), '"id": "<ID>"'),  # JSON
    (re.compile(r' \(\d{1,2}\)'), ' (<ID>)'),  # Labels with Small IDs
]

def cli_assert_normalize_ids(test: edq.testing.unittest.BaseTest, expected: str, actual: str, **kwargs: typing.Any) -> None:
    """
    Normalize IDs (as output from a standard CLI,
    and then use edq.testing.asserts.content_equals_normalize().
    """

    for (pattern, replacement) in ID_SUBS:
        expected = re.sub(pattern, replacement, expected)
        actual = re.sub(pattern, replacement, actual)

    edq.testing.asserts.content_equals_normalize(test, expected, actual)
