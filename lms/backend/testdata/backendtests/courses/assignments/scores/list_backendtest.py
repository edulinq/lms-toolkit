import lms.backend.testing
import lms.model.testdata.scores

def test_courses_assignments_scores_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing assignments scores. """

    scores = lms.model.testdata.scores.COURSE_ASSIGNMENT_SCORES_UNRESOLVED

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_id': '110000000',
                'assignment_id': '110000100',
            },
            [
                scores['Course 101']['Homework 0']['course-student'],
            ],
            None,
        ),

        (
            {
                'course_id': '120000000',
                'assignment_id': '120000100',
            },
            [
            ],
            None,
        ),

        (
            {
                'course_id': '130000000',
                'assignment_id': '130000100',
            },
            [
                scores['Extra Course']['Assignment 1']['extra-course-student-1'],
                scores['Extra Course']['Assignment 1']['extra-course-student-2'],
                scores['Extra Course']['Assignment 1']['extra-course-student-3'],
                scores['Extra Course']['Assignment 1']['extra-course-student-4'],
            ],
            None,
        ),

        (
            {
                'course_id': '130000000',
                'assignment_id': '130000200',
            },
            [
                scores['Extra Course']['Assignment 2']['extra-course-student-1'],
                scores['Extra Course']['Assignment 2']['extra-course-student-2'],
                scores['Extra Course']['Assignment 2']['extra-course-student-3'],
                scores['Extra Course']['Assignment 2']['extra-course-student-4'],
            ],
            None,
        ),

        (
            {
                'course_id': '130000000',
                'assignment_id': '130000300',
            },
            [
                scores['Extra Course']['Assignment 3']['extra-course-student-1'],
                scores['Extra Course']['Assignment 3']['extra-course-student-2'],
                scores['Extra Course']['Assignment 3']['extra-course-student-3'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_assignments_scores_list, test_cases)
