import lms.backend.testing
import lms.model.courses
import lms.model.testdata.groupsets

def test_courses_groupsets_resolve_and_list_base(test: lms.backend.testing.BackendTest):
    """ Test the base functionality of resolving and listing course groupsets. """

    # [(kwargs (and overrides), expected, error substring), ...]
    test_cases = [
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '110000000'),
            },
            [
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '120000000'),
            },
            [
            ],
            None,
        ),
        (
            {
                'course_query': lms.model.courses.CourseQuery(id = '130000000'),
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 3'],
            ],
            None,
        ),

        (
            {
                'course_query': lms.model.courses.CourseQuery(name = 'Extra Course'),
            },
            [
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 1'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 2'],
                lms.model.testdata.groupsets.COURSE_GROUPSETS['Extra Course']['Group Set 3'],
            ],
            None,
        ),
    ]

    test.base_request_test(test.backend.courses_groupsets_resolve_and_list, test_cases)
