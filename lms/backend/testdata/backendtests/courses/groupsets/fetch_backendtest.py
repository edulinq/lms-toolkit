import lms.backend.testing
import lms.model.testdata.groupsets

def test_courses_groupsets_fetch_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of fetching course groupsets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        # Base
        (
            {
                'course_id': '130000000',
                'groupset_id': '131010100',
            },
            lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
            None,
        ),

        # Miss
        (
            {
                'course_id': '110000000',
                'groupset_id': '999',
            },
            None,
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_fetch, test_cases)
