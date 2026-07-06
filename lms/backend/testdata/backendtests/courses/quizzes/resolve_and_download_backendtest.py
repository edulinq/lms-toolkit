import lms.backend.testing
import lms.backend.testdata.backendtests.courses.quizzes.common
import lms.model.assignments
import lms.model.courses
import lms.model.testdata.quizzes

def test_courses_quizzes_resolve_and_download_base(test: lms.backend.testing.BackendTest) -> None:
    """ Test the base functionality of resolving and downloading course quizzes. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'quiz_query': lms.model.assignments.AssignmentQuery(id = '110000200'),
            },
            lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'quiz_query': lms.model.assignments.AssignmentQuery(name = 'Regular Expressions'),
            },
            lms.model.testdata.quizzes.COURSE_QUIZZES['Course 101']['Regular Expressions'],
            None,
        ),

        # Miss
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'ZZZ'),
                'quiz_query': lms.model.assignments.AssignmentQuery(name = 'Regular Expressions'),
            },
            None,
            'Could not resolve course query',
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'quiz_query': lms.model.assignments.AssignmentQuery(name = 'ZZZ'),
            },
            None,
            'Could not resolve quiz query',
        ),
    ]

    test.base_request_test(test.backend.courses_quizzes_resolve_and_download, test_cases,
        actual_clean_func = lms.backend.testdata.backendtests.courses.quizzes.common._sketch_quiz,
        expected_clean_func = lms.backend.testdata.backendtests.courses.quizzes.common._sketch_quiz,
    )
