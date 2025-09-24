import lms.api.user.testing

ASSIGNMENTS = {
    '67890': {
        "assignment_group_id": "200001",
        "description": "The first assignment.",
        "due_at": "1970-01-01T01:01:01Z",
        "id": "67890",
        "name": "Assignment 1",
        "points_possible": 1.0,
        "position": 2,
        "published": True
    },
    '67891': {
        "assignment_group_id": "200001",
        "description": None,
        "due_at": None,
        "id": "67891",
        "name": "Quiz 1",
        "points_possible": 1.0,
        "position": 3,
        "published": False
    },
    '67892': {
        "assignment_group_id": "200001",
        "description": "The third assignment (has submissions).",
        "due_at": "1970-01-01T01:01:01Z",
        "id": "67892",
        "name": "Assignment 3",
        "points_possible": 1.0,
        "position": 2,
        "published": True
    }
}

SCORES = {
    '67890': {
        '10001': {
            "assignment": ASSIGNMENTS['67890'],
            "grade": "1",
            "graded_at": "1970-01-01T01:01:01Z",
            "id": "50000001",
            "score": 1.0,
            "submitted_at": "1970-01-01T01:01:01Z",
            "user": lms.api.user.testing.USERS['10001'],
        },
        '10002': {
            "assignment": ASSIGNMENTS['67890'],
            "grade": "1",
            "graded_at": "1970-01-01T01:01:01Z",
            "id": "50000002",
            "score": 0.5,
            "submitted_at": "1970-01-01T01:01:01Z",
            "user": lms.api.user.testing.USERS['10002'],
        }
    }
}
