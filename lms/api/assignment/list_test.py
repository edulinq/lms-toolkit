import lms.api.testing
import lms.api.assignment.list
import lms.api.assignment.testing

class AssignmentListTest(lms.api.testing.HTTPTest):
    """ Test listing course assignments. """

    def test_assignment_list_base(self):
        """ Test the base functionality of listing assignments. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            (
                {},
                [
                    lms.api.assignment.testing.ASSIGNMENTS['67890'],
                    lms.api.assignment.testing.ASSIGNMENTS['67891'],
                    lms.api.assignment.testing.ASSIGNMENTS['67892'],
                ],
                None,
            ),
        ]

        self.base_request_test(lms.api.assignment.list.request, test_cases)
