import lms.backend.testing
import lms.model.testdata.courses

def test_courses_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of listing courses. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {},
            [
                lms.model.testdata.courses.COURSES['Course 101'],
                lms.model.testdata.courses.COURSES['Course Using Different Languages'],
                lms.model.testdata.courses.COURSES['Extra Course'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_list, test_cases)
