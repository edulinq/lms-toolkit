import lms.backend.testing
import lms.model.courses

def test_courses_syllabus_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting a course's syllabus. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
            },
            'A sample course syllabus.',
            None,
        ),

        # Empty
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
            },
            None,
            None,
        ),

        # Miss
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '999'),
            },
            None,
            'Could not resolve course query',
        ),
    ]

    test.base_request_test(test.backend.courses_syllabus_get, test_cases)
