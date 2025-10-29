import lms.backend.testing
import lms.model.courses
import lms.model.testdata.scores

def test_courses_users_scores_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing users' scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'user_query': lms.model.users.UserQuery(id = '100050000'),
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'user_query': lms.model.users.UserQuery(id = '100050000'),
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
                'user_query': lms.model.users.UserQuery(id = '100050000'),
            },
            [
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'user_query': lms.model.users.UserQuery(id = '100060000'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-1'],
                scores['Extra Course']['Assignment 2']['extra-course-student-1'],
                scores['Extra Course']['Assignment 3']['extra-course-student-1'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'user_query': lms.model.users.UserQuery(id = '100070000'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-2'],
                scores['Extra Course']['Assignment 2']['extra-course-student-2'],
                scores['Extra Course']['Assignment 3']['extra-course-student-2'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'user_query': lms.model.users.UserQuery(id = '100080000'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-3'],
                scores['Extra Course']['Assignment 2']['extra-course-student-3'],
                scores['Extra Course']['Assignment 3']['extra-course-student-3'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'user_query': lms.model.users.UserQuery(id = '100090000'),
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-4'],
                scores['Extra Course']['Assignment 2']['extra-course-student-4'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_users_scores_resolve_and_list, test_cases)
