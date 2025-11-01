import lms.backend.testing
import lms.model.groupsets

def test_courses_groupsets_resolve_and_delete_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of deleting group sets (with resolution). """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'Group Set 1'),
            },
            True,
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'groupset_query': lms.model.groupsets.GroupSetQuery(name = 'ZZZ'),
            },
            None,
            'Could not resolve group set query',
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_resolve_and_delete, test_cases)
