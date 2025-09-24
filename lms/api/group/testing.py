GROUPINGS = [
    {
        "id": 30001,
        "name": "Group 1 - No Leader"
    },
    {
        "id": 30002,
        "name": "Group 2 - Leader"
    }
]

GROUPS = {
    '30001': [
        {
            "id": "300010",
            "name": "Group 1 - No Leader 1"
        },
        {
            "id": "300011",
            "name": "Group 1 - No Leader 2"
        },
    ],
    '30002': [
        {
            "id": "300020",
            "name": "Group 2 - Leader 1"
        },
    ],
}

GROUP_MEMBERSHIP = {
    '300010': [
        {
            "id": "10001",
            "login_id": "aalvarez@ucsc.edu",
            "name": "Alice Alvarez",
            "sis_user_id": "1000001"
        }
    ],
    '300011': [
        {
            "id": "10002",
            "login_id": "bburnquist@ucsc.edu",
            "name": "Bob Burnquist",
            "sis_user_id": "1000002"
        }
    ],
    '300020': [
        {
            "id": "10001",
            "login_id": "aalvarez@ucsc.edu",
            "name": "Alice Alvarez",
            "sis_user_id": "1000001"
        },
        {
            "id": "10002",
            "login_id": "bburnquist@ucsc.edu",
            "name": "Bob Burnquist",
            "sis_user_id": "1000002"
        }
    ],
}

GROUPING_MEMBERSHIPS = {
    '30001': [
        {
            "email": "aalvarez@ucsc.edu",
            "group_name": "Group 1 - No Leader 1",
            "lms_group_id": "300010"
        },
        {
            "email": "bburnquist@ucsc.edu",
            "group_name": "Group 1 - No Leader 2",
            "lms_group_id": "300011"
        },
    ],
    '30002': [
        {
            "email": "aalvarez@ucsc.edu",
            "group_name": "Group 2 - Leader 1",
            "lms_group_id": "300020"
        },
        {
            "email": "bburnquist@ucsc.edu",
            "group_name": "Group 2 - Leader 1",
            "lms_group_id": "300020"
        }
    ],
}
