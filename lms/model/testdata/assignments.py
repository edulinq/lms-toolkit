import lms.model.assignments

# {course_name: {name: assignment, ...}, ...}
COURSE_ASSIGNMENTS = {
    'Course 101': {
        'Homework 0': lms.model.assignments.Assignment(
            id = '1',
            name = 'Homework 0',
            points_possible = 2.0,
            position = 1,
            group_id = '1',
        ),
    },
    'Course Using Different Languages': {
        'A Simple Bash Assignment': lms.model.assignments.Assignment(
            id = '2',
            name = 'A Simple Bash Assignment',
            points_possible = 10.0,
            position = 1,
            group_id = '2'
        ),
        'A Simple C++ Assignment': lms.model.assignments.Assignment(
            id = '3',
            name = 'A Simple C++ Assignment',
            points_possible = 10.0,
            position = 2,
            group_id = '2'
        ),
        'A Simple Java Assignment': lms.model.assignments.Assignment(
            id = '4',
            name = 'A Simple Java Assignment',
            points_possible = 10.0,
            position = 3,
            group_id = '2'
        ),
    }
}
