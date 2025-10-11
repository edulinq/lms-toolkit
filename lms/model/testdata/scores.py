import edq.util.time

import lms.model.assignments
import lms.model.scores
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
                graded_date = edq.util.time.Timestamp(1759864852000),
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
                assignment_query = lms.model.assignments.AssignmentQuery(id = '1', name = 'Homework 0'),
                user_query = lms.model.users.UserQuery(id = '6', name = 'course-student', email = 'course-student@test.edulinq.org'),
                score = 2.0,
                graded_date = edq.util.time.Timestamp(1759864852000),
            ),
        },
    },
}
