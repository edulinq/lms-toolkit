import lms.backend.testing
import lms.model.scores
import lms.model.testdata.scores

def test_courses_gradebook_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing a course's gradebook. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '110000000',
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course 101'],
            None,
        ),
        (
            {
                'course_id': '120000000',
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Course Using Different Languages'],
            None,
        ),
        (
            {
                'course_id': '130000000',
            },
            lms.model.testdata.scores.COURSE_GRADEBOOKS['Extra Course'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '999',
            },
            None,
            'Could not resolve course query',
        ),
    ]

    test.base_request_test(test.backend.courses_gradebook_list, test_cases)
