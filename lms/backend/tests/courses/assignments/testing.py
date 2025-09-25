import datetime

import edq.util.time

import lms.model.assignments

ASSIGNMENTS = {
    '67890': lms.model.assignments.Assignment(
        id = '67890',
        name = 'Assignment 1',
        description = 'The first assignment.',
        open_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        close_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        due_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        points_possible = 1.0,
        position = 2,
        group_id = '200001',
    ),
    '67891': lms.model.assignments.Assignment(
        id = '67891',
        name = 'Quiz 1',
        description = None,
        due_date = None,
        points_possible = 1.0,
        position = 3,
        group_id = '200001',
    ),
    '67892': lms.model.assignments.Assignment(
        id = '67892',
        name = 'Assignment 3',
        description = 'The third assignment (has submissions).',
        open_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        close_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        due_date = edq.util.time.Timestamp.from_pytime(datetime.datetime.fromisoformat('1970-01-01T01:01:01Z')),
        points_possible = 1.0,
        position = 2,
        group_id = '200001',
    ),
}
