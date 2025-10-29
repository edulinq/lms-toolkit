import lms.backend.testing
import lms.model.assignments
import lms.model.courses
import lms.model.scores
import lms.model.testdata.assignments
import lms.model.testdata.users
import lms.model.testdata.scores
import lms.model.users

def test_courses_gradebook_get_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of getting a course's gradebook. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'].assignments,
                'user_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'].users,
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),

        # Course Query
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Course 101'),
                'assignment_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'].assignments,
                'user_queries': lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'].users,
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),

        # No Queries
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
                'assignment_queries': [],
                'user_queries': [],
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),

        # Miss
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '999'),
                'assignment_queries': [],
                'user_queries': [],
            },
            None,
            'Could not resolve course query',
        ),

        # Single Assignment
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'assignment_queries': [
                    lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
                ],
                'user_queries': [],
            },
            _build_gradebook('Extra Course', ['Assignment 2'], None),
            None,
        ),

        # Single User
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'assignment_queries': [],
                'user_queries': [
                    lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
                ],
            },
            _build_gradebook('Extra Course', None, ['extra-course-student-2']),
            None,
        ),

        # Doubles
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
                'assignment_queries': [
                    lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
                    lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 3'].to_query(),
                ],
                'user_queries': [
                    lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
                    lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'].to_query(),
                ],
            },
            _build_gradebook('Extra Course', ['Assignment 1', 'Assignment 3'], ['extra-course-student-1', 'extra-course-student-4']),
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_get, test_cases)

def _build_gradebook(course_name, allowed_assignment_names, allowed_user_names):
    assignment_queries = []
    for assignment in sorted(lms.model.testdata.assignments.COURSE_ASSIGNMENTS[course_name].values()):
        if ((allowed_assignment_names is None) or (assignment.name in allowed_assignment_names)):
            assignment_queries.append(assignment.to_query())

    user_queries = []
    for user in sorted(lms.model.testdata.users.COURSE_USERS[course_name].values()):
        if (not user.is_student()):
            continue

        if ((allowed_user_names is None) or (user.name in allowed_user_names)):
            user_queries.append(user.to_query())

    gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

    for (assignment_name, user_scores) in lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES[course_name].items():
        if ((allowed_assignment_names is not None) and (assignment_name not in allowed_assignment_names)):
            continue

        for (user_name, score) in user_scores.items():
            if ((allowed_user_names is not None) and (user_name not in allowed_user_names)):
                continue

            gradebook.add(score)

    return gradebook
