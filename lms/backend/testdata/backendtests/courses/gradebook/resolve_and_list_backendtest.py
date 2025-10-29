import lms.backend.testing
import lms.model.scores
import lms.model.testdata.scores

def test_courses_gradebook_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing a course's gradebook. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course Using Different Languages'],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Extra Course'],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
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

    test.base_request_test(test.backend.courses_gradebook_resolve_and_list, test_cases)
