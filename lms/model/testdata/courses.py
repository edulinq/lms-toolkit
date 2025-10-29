import typing

import lms.model.courses

# {course_name: course, ...}
COURSES: typing.Dict[str, lms.model.courses.Course] = {
    'Course 101': lms.model.courses.Course(
        id = 110000000,
        name = 'Course 101',
    ),
    'Course Using Different Languages': lms.model.courses.Course(
        id = 120000000,
        name = 'Course Using Different Languages',
    ),
    'Extra Course': lms.model.courses.Course(
        id = 130000000,
        name = 'Extra Course',
    ),
}
