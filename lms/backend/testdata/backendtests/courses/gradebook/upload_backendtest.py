import lms.backend.testing
import lms.model.courses
import lms.model.scores
import lms.model.testdata.assignments
import lms.model.testdata.scores
import lms.model.testdata.users

def test_courses_gradebook_upload_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of uploading gradebooks. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '130000000',
                'gradebook': _get_base_gradebook(),
            },
            4,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_upload, test_cases)

def test_courses_gradebook_resolve_and_upload_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and uploading gradebooks. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
                'gradebook': _get_base_gradebook(),
            },
            4,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_resolve_and_upload, test_cases)

def _get_base_gradebook():
    base_assignments = [
        lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 1'].to_query(),
        lms.model.testdata.assignments.COURSE_ASSIGNMENTS['Extra Course']['Assignment 2'].to_query(),
    ]

    base_users = [
        lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-1'].to_query(),
        lms.model.testdata.users.COURSE_USERS['Extra Course']['extra-course-student-2'].to_query(),
    ]

    base_gradebook = lms.model.scores.Gradebook(base_assignments, base_users)

    base_gradebook.add(lms.model.scores.AssignmentScore(score = 1.0,
            assignment_query = base_assignments[0], user_query = base_users[0]))
    base_gradebook.add(lms.model.scores.AssignmentScore(score = 0.5,
            assignment_query = base_assignments[0], user_query = base_users[1]))
    base_gradebook.add(lms.model.scores.AssignmentScore(score = 1.0, comment = 'extra-course-student-1 comment',
            assignment_query = base_assignments[1], user_query = base_users[0]))
    base_gradebook.add(lms.model.scores.AssignmentScore(score = 0.5, comment = 'extra-course-student-2 comment',
            assignment_query = base_assignments[1], user_query = base_users[1]))

    return base_gradebook
