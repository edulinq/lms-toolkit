import lms.api.testing
import lms.api.group.listgroups
import lms.api.group.testing

class ListGroups(lms.api.testing.HTTPTest):
    """ Test listing groups. """

    def test_list_groups_base(self):
        """ Test the base functionality of listing groups. """

        # [(kwargs (and overrides), expected, error substring), ...]
        test_cases = [
            # Empty / All

            (
                {},
                lms.api.group.testing.GROUPS['30001'] + lms.api.group.testing.GROUPS['30002'],
                None,
            ),

            # Grouping

            (
                {
                    'grouping': '30001',
                },
                lms.api.group.testing.GROUPS['30001'],
                None,
            ),

            (
                {
                    'grouping': 'Group 1 - No Leader',
                },
                lms.api.group.testing.GROUPS['30001'],
                None,
            ),

            (
                {
                    'grouping': '30002',
                },
                lms.api.group.testing.GROUPS['30002'],
                None,
            ),
        ]

        self.base_request_test(lms.api.group.listgroups.request, test_cases)
