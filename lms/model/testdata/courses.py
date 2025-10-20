import typing

import lms.model.courses

# {course_name: course, ...}
COURSES: typing.Dict[str, lms.model.courses.Course] = {
    'Course 101': lms.model.courses.Course(
        id = 1,
        name = 'Course 101',
    ),
    'Course Using Different Languages': lms.model.courses.Course(
        id = 2,
        name = 'Course Using Different Languages',
    ),
    'Extra Course': lms.model.courses.Course(
        id = 3,
        name = 'Extra Course',
    ),
}
