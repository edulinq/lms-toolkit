import lms.backend.testing
import lms.model.courses
import lms.model.testdata.courses

def test_courses_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting courses. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Empty
        (
            {
                'course_queries': [],
            },
            [
            ],
            None,
        ),

        # Base - List
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(id = '120000000'),
                    lms.model.courses.CourseQuery(id = '130000000'),
                ],
            },
            [
                lms.model.testdata.courses.COURSES['Course Using Different Languages'],
                lms.model.testdata.courses.COURSES['Extra Course'],
            ],
            None,
        ),

        # Base - Fetch
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(id = '120000000'),
                ],
            },
            [
                lms.model.testdata.courses.COURSES['Course Using Different Languages'],
            ],
            None,
        ),

        # Query - Name
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(name = 'Course 101'),
                ],
            },
            [
                lms.model.testdata.courses.COURSES['Course 101'],
            ],
            None,
        ),

        # Query - Label
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(name = 'Course 101', id = '110000000'),
                ],
            },
            [
                lms.model.testdata.courses.COURSES['Course 101'],
            ],
            None,
        ),

        # Miss - ID
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(id = 999),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Query
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Miss - Partial Match
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(id = '120000000', name = 'ZZZ'),
                ],
            },
            [
            ],
            None,
        ),

        # Multiple Match
        (
            {
                'course_queries': [
                    lms.model.courses.CourseQuery(id = '110000000'),
                    lms.model.courses.CourseQuery(name = 'Course 101'),
                ],
            },
            [
                lms.model.testdata.courses.COURSES['Course 101'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_get, test_cases)
