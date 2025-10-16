import typing

import edq.util.time

import lms.model.assignments
import lms.model.scores
import lms.model.testdata.assignments
import lms.model.testdata.users
import lms.model.users

# {course_id: {assignment_id: {user_email: score, ...}, ...}
COURSE_ASSIGNMENT_SCORES = {
    '1': {
        '1': {
            'course-student@test.edulinq.org': lms.model.scores.AssignmentScore(
                id = '1',
                assignment_query = lms.model.assignments.AssignmentQuery(id = '1'),
                user_query = lms.model.users.UserQuery(id = '6'),
                score = 2.0,
                graded_date = edq.util.time.Timestamp(1697406273000),
            ),
        },
    },
}

# {course_id: {assignment_id: {user_email: score, ...}, ...}
COURSE_ASSIGNMENT_SCORES_RESOLVED = {
    '1': {
        '1': {
            'course-student@test.edulinq.org': lms.model.scores.AssignmentScore(
                id = '1',
                assignment_query = lms.model.testdata.assignments.COURSE_ASSIGNMENTS['1']['1'].to_query(),
                user_query = lms.model.testdata.users.COURSE_USERS['1']['course-student@test.edulinq.org'].to_query(),
                score = 2.0,
                graded_date = edq.util.time.Timestamp(1697406273000),
            ),
        },
    },
}

# {course_id: gradebook}
COURSE_GRADEBOOKS = {}

# {course_id: gradebook}
COURSE_GRADEBOOKS_RESOLVED = {}

def _load_gradebooks() -> None:
    for course_id in ['1', '2']:
        assignments: typing.Any = lms.model.testdata.assignments.COURSE_ASSIGNMENTS[course_id].values()
        assignment_queries = list(sorted([lms.model.assignments.AssignmentQuery(id = assignment.id) for assignment in assignments]))

        users: typing.Any = lms.model.testdata.users.COURSE_USERS[course_id].values()
        users = list(filter(lambda user: user.is_student(), users))
        user_queries = list(sorted([lms.model.users.UserQuery(id = user.id) for user in users]))

        gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

        for assignments_users_scores in COURSE_ASSIGNMENT_SCORES.get(course_id, {}).values():
            for score in assignments_users_scores.values():
                gradebook.add(score)

        COURSE_GRADEBOOKS[course_id] = gradebook

def _load_resolved_gradebooks() -> None:
    for course_id in ['1', '2']:
        assignments: typing.Any = lms.model.testdata.assignments.COURSE_ASSIGNMENTS[course_id].values()
        assignment_queries = list(sorted([assignment.to_query() for assignment in assignments]))

        users: typing.Any = lms.model.testdata.users.COURSE_USERS[course_id].values()
        users = list(filter(lambda user: user.is_student(), users))
        user_queries = list(sorted([user.to_query() for user in users]))

        gradebook = lms.model.scores.Gradebook(assignment_queries, user_queries)

        for assignments_users_scores in COURSE_ASSIGNMENT_SCORES_RESOLVED.get(course_id, {}).values():
            for score in assignments_users_scores.values():
                gradebook.add(score)

        COURSE_GRADEBOOKS_RESOLVED[course_id] = gradebook

_load_gradebooks()
_load_resolved_gradebooks()
