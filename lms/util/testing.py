import re
import typing

import edq.testing.asserts
import edq.testing.unittest
import edq.util.json

import lms.model.testdata.quizzes

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

def cli_assert_quiz_groups(test: edq.testing.unittest.BaseTest, expected: str, actual: str, **kwargs: typing.Any) -> None:
    """
    Verify that the quiz groups (in JSON) matches the expected test quiz groups.
    """

    expected_list = edq.util.json.loads(edq.util.json.dumps(lms.model.testdata.quizzes.ORDERED_QUIZ_GROUPS['Regular Expressions']))
    actual_list = edq.util.json.loads(actual)

    # Remove an extra field.
    for group in expected_list:
        group.pop('extra_fields', None)

    test.assertListEqual(expected_list, actual_list)

def cli_assert_quiz_questions(test: edq.testing.unittest.BaseTest, expected: str, actual: str, **kwargs: typing.Any) -> None:
    """
    Verify that the quiz questions (in JSON) matches the expected test quiz questions.
    """

    expected_list = edq.util.json.loads(edq.util.json.dumps(lms.model.testdata.quizzes.ORDERED_QUIZ_QUESTIONS['Regular Expressions']))
    actual_list = edq.util.json.loads(actual)

    # Remove extra fields.
    for question in expected_list:
        question.pop('extra_fields', None)
        question.pop('group_id', None)

    test.assertListEqual(expected_list, actual_list)
