import lms.model.assignments

# {course_id: {name: assignment, ...}, ...}
COURSE_ASSIGNMENTS = {
    '1': {
        'Homework 0': lms.model.assignments.Assignment(
            group_id = "1",
            id = "1",
            name = "Homework 0",
            points_possible = 2.0,
            position = 1,
        ),
    },
}
