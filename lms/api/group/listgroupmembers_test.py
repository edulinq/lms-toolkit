import lms.api.testing
import lms.api.group.listgroupmembers
import lms.api.group.testing

class ListGroupMembers(lms.api.testing.HTTPTest):
    """ Test listing group members. """

    def test_list_group_members_base(self):
        """ Test the base functionality of listing group members. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty

            (
                {
                    'group': 'ZZZ',
                },
                [],
                None,
            ),

            # Base

            (
                {
                    'group': '300010',
                },
                lms.api.group.testing.GROUP_MEMBERSHIP['300010'],
                None,
            ),

            (
                {
                    'group': '300011',
                },
                lms.api.group.testing.GROUP_MEMBERSHIP['300011'],
                None,
            ),

            (
                {
                    'group': 'Group 2 - Leader 1',
                },
                lms.api.group.testing.GROUP_MEMBERSHIP['300020'],
                None,
            ),
        ]

        self.base_request_test(lms.api.group.listgroupmembers.request, test_cases)
