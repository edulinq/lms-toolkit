import lms.backend.testing

def test_courses_syllabus_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching a course's syllabus. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
            },
            'A sample course syllabus.',
            None,
        ),

        # Empty
        (
            {
                'course_id': '120000000',
            },
            None,
            None,
        ),

        # Miss
        (
            {
                'course_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_syllabus_fetch, test_cases)
