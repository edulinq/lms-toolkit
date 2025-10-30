import typing

import edq.util.time

import lms.model.assignments
import lms.model.scores
import lms.model.testdata.assignments
import lms.model.testdata.courses
import lms.model.testdata.users
import lms.model.users

# {course_name: {assignment_name: {user_name: score, ...}, ...}
COURSE_ASSIGNMENT_SCORES: typing.Dict[str, typing.Dict[str, typing.Dict[str, lms.model.scores.AssignmentScore]]] = {}

COURSE_ASSIGNMENT_SCORES['Course 101'] = {
    'Homework 0': {
        'course-student': lms.model.scores.AssignmentScore(
            id = '110050101',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Course 101']['Homework 0'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Course 101']['course-student'].to_query(),
            score = 2.0,
            graded_date = edq.util.time.Timestamp(1697406273000),
        ),
    },
}

COURSE_ASSIGNMENT_SCORES['Extra Course'] = {
    'Assignment 1': {
        'extra-course-student-1': lms.model.scores.AssignmentScore(
            id = '130060101',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
            score = 10.0,
            graded_date = edq.util.time.Timestamp(1100000000000),
        ),
        'extra-course-student-2': lms.model.scores.AssignmentScore(
            id = '130070101',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
            score = 7.5,
            graded_date = edq.util.time.Timestamp(1100000000000),
        ),
        'extra-course-student-3': lms.model.scores.AssignmentScore(
            id = '130080101',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'].to_query(),
            score = 5.0,
            graded_date = edq.util.time.Timestamp(1100000000000),
        ),
        'extra-course-student-4': lms.model.scores.AssignmentScore(
            id = '130090101',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'].to_query(),
            score = 0.0,
            graded_date = edq.util.time.Timestamp(1100000000000),
        ),
    },
    'Assignment 2': {
        'extra-course-student-1': lms.model.scores.AssignmentScore(
            id = '130060201',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
            score = 20.0,
            graded_date = edq.util.time.Timestamp(1200000000000),
        ),
        'extra-course-student-2': lms.model.scores.AssignmentScore(
            id = '130070201',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
            score = 15.0,
            graded_date = edq.util.time.Timestamp(1200000000000),
        ),
        'extra-course-student-3': lms.model.scores.AssignmentScore(
            id = '130080201',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'].to_query(),
            score = 10.0,
            graded_date = edq.util.time.Timestamp(1200000000000),
        ),
        'extra-course-student-4': lms.model.scores.AssignmentScore(
            id = '130090201',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-4'].to_query(),
            score = 0.0,
            graded_date = edq.util.time.Timestamp(1200000000000),
        ),
    },
    'Assignment 3': {
        'extra-course-student-1': lms.model.scores.AssignmentScore(
            id = '130060301',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 3'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
            score = 30.0,
            graded_date = edq.util.time.Timestamp(1300000000000),
        ),
        'extra-course-student-2': lms.model.scores.AssignmentScore(
            id = '130070301',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 3'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
            score = 22.5,
            graded_date = edq.util.time.Timestamp(1300000000000),
        ),
        'extra-course-student-3': lms.model.scores.AssignmentScore(
            id = '130080301',
            assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 3'].to_query(),
            user_query = lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-3'].to_query(),
            score = 15.0,
            graded_date = edq.util.time.Timestamp(1300000000000),
        ),
    },
}

# {course_name: {assignment_name: {user_name: score, ...}, ...}
COURSE_ASSIGNMENT_SCORES_UNRESOLVED: typing.Dict[str, typing.Dict[str, typing.Dict[str, lms.model.scores.AssignmentScore]]] = {}

# {course_name: gradebook}
COURSE_GRADEBOOKS: typing.Dict[str, lms.model.scores.Gradebook] = {}

# {course_name: gradebook}
COURSE_GRADEBOOKS_UNRESOLVED: typing.Dict[str, lms.model.scores.Gradebook] = {}

def _load_unresolved_scores() -> None:
    """ Load unresolved scores from resolved scores. """

    for (course_name, assignment_scores) in COURSE_ASSIGNMENT_SCORES.items():
        if (course_name not in COURSE_ASSIGNMENT_SCORES_UNRESOLVED):
            COURSE_ASSIGNMENT_SCORES_UNRESOLVED[course_name] = {}

        for (assignment_name, user_scores) in assignment_scores.items():
            if (assignment_name not in COURSE_ASSIGNMENT_SCORES_UNRESOLVED[course_name]):
                COURSE_ASSIGNMENT_SCORES_UNRESOLVED[course_name][assignment_name] = {}

            for (user_name, old_score) in user_scores.items():
                if ((old_score.assignment_query is None) or (old_score.user_query is None)):
                    raise ValueError(f"None query for {course_name}.{assignment_name}.{user_name}.")

                new_score = lms.model.scores.AssignmentScore(
                    id = old_score.id,
                    assignment_query = lms.model.assignments.AssignmentQuery(id = old_score.assignment_query.id),
                    user_query = lms.model.users.UserQuery(id = old_score.user_query.id),
                    score = old_score.score,
                    graded_date = old_score.graded_date,
                )

                COURSE_ASSIGNMENT_SCORES_UNRESOLVED[course_name][assignment_name][user_name] = new_score

def _load_gradebooks(
        gradebooks: typing.Dict[str, lms.model.scores.Gradebook],
        scores: typing.Dict[str, typing.Dict[str, typing.Dict[str, lms.model.scores.AssignmentScore]]],
        get_assignment_query: typing.Callable,
        get_user_query: typing.Callable,
        ) -> None:
    """ Load gradebooks from scores. """

    for course_name in lms.model.testdata.courses.COURSES.keys():
        assignments: typing.Any = lms.model.testdata.assignments.COURSE_ASSIGNMENTS[course_name].values()
        assignment_queries = list(sorted([get_assignment_query(assignment) for assignment in assignments]))

        users: typing.Any = lms.model.testdata.users.COURSE_USERS[course_name].values()
        users = list(filter(lambda user: user.is_student(), users))
        user_queries = list(sorted([get_user_query(user) for user in users]))

        gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

        for assignments_users_scores in scores.get(course_name, {}).values():
            for score in assignments_users_scores.values():
                gradebook.add(score)

        gradebooks[course_name] = gradebook

_load_unresolved_scores()

_load_gradebooks(
    COURSE_GRADEBOOKS,
    COURSE_ASSIGNMENT_SCORES,
    lambda assignment: assignment.to_query(),
    lambda user: user.to_query(),
)

_load_gradebooks(
    COURSE_GRADEBOOKS_UNRESOLVED,
    COURSE_ASSIGNMENT_SCORES_UNRESOLVED,
    lambda assignment: lms.model.assignments.AssignmentQuery(id = assignment.id),
    lambda user: lms.model.users.UserQuery(id = user.id),
)
