import lms.api.testing
import lms.api.group.listgroupings
import lms.api.group.testing

class ListGroupings(lms.api.testing.HTTPTest):
    """ Test listing groupings. """

    def test_list_groupings_base(self):
        """ Test the base functionality of listing groupings. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Base

            (
                {},
                lms.api.group.testing.GROUPINGS,
                None,
            ),
        ]

        self.base_request_test(lms.api.group.listgroupings.request, test_cases)
