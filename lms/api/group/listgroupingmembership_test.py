import lms.api.testing
import lms.api.group.listgroupingmembership
import lms.api.group.testing

class ListGroupingMembership(lms.api.testing.HTTPTest):
    """ Test listing grouping membership. """

    def test_list_grouping_membership_base(self):
        """ Test the base functionality of listing grouping membership. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Missing

            (
                {
                    'grouping': 'ZZZ',
                },
                [],
                None,
            ),

            # Base

            (
                {
                    'grouping': '30001',
                },
                lms.api.group.testing.GROUPING_MEMBERSHIPS['30001'],
                None,
            ),

            (
                {
                    'grouping': '30002',
                },
                lms.api.group.testing.GROUPING_MEMBERSHIPS['30002'],
                None,
            ),

            # Resolve

            (
                {
                    'grouping': 'Group 1 - No Leader',
                },
                lms.api.group.testing.GROUPING_MEMBERSHIPS['30001'],
                None,
            ),
        ]

        self.base_request_test(lms.api.group.listgroupingmembership.request, test_cases)
