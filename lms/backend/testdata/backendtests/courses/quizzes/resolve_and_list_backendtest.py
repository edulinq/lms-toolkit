import lms.backend.testing
import lms.model.courses
import lms.model.testdata.quizzes

def test_courses_quizzes_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
            },
            [
                lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_resolve_and_list, test_cases)
