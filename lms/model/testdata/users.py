import typing

import lms.model.users

# {course_name: {user_name: user, ...}, ...}
COURSE_USERS: typing.Dict[str, typing.Dict[str, lms.model.users.CourseUser]] = {}

COURSE_USERS['Course 101'] = {
    'course-admin': lms.model.users.CourseUser(
        email = 'course-admin@test.edulinq.org',
        id = '100010000',
        name = 'course-admin',
        role = lms.model.users.CourseRole.ADMIN,
    ),
    'course-grader': lms.model.users.CourseUser(
        email = 'course-grader@test.edulinq.org',
        id = '100020000',
        name = 'course-grader',
        role = lms.model.users.CourseRole.GRADER,
    ),
    'course-other': lms.model.users.CourseUser(
        email = 'course-other@test.edulinq.org',
        id = '100030000',
        name = 'course-other',
        role = lms.model.users.CourseRole.OTHER,
    ),
    'course-owner': lms.model.users.CourseUser(
        email = 'course-owner@test.edulinq.org',
        id = '100040000',
        name = 'course-owner',
        role = lms.model.users.CourseRole.OWNER,
    ),
    'course-student': lms.model.users.CourseUser(
        email = 'course-student@test.edulinq.org',
        id = '100050000',
        name = 'course-student',
        role = lms.model.users.CourseRole.STUDENT,
    ),
}

COURSE_USERS['Course Using Different Languages'] = COURSE_USERS['Course 101']

COURSE_USERS['Extra Course'] = {
    'course-owner': COURSE_USERS['Course 101']['course-owner'],
    'extra-course-student-1': lms.model.users.CourseUser(
        email = 'extra-course-student-1@test.edulinq.org',
        id = '100060000',
        name = 'extra-course-student-1',
        role = lms.model.users.CourseRole.STUDENT,
    ),
    'extra-course-student-2': lms.model.users.CourseUser(
        email = 'extra-course-student-2@test.edulinq.org',
        id = '100070000',
        name = 'extra-course-student-2',
        role = lms.model.users.CourseRole.STUDENT,
    ),
    'extra-course-student-3': lms.model.users.CourseUser(
        email = 'extra-course-student-3@test.edulinq.org',
        id = '100080000',
        name = 'extra-course-student-3',
        role = lms.model.users.CourseRole.STUDENT,
    ),
    'extra-course-student-4': lms.model.users.CourseUser(
        email = 'extra-course-student-4@test.edulinq.org',
        id = '100090000',
        name = 'extra-course-student-4',
        role = lms.model.users.CourseRole.STUDENT,
    ),
}

# {user_name: user, ...}
SERVER_USERS = {
    'course-admin': lms.model.users.ServerUser(
        email = 'course-admin@test.edulinq.org',
        id = '100010000',
        name = 'course-admin',
    ),
    'course-grader': lms.model.users.ServerUser(
        email = 'course-grader@test.edulinq.org',
        id = '100020000',
        name = 'course-grader',
    ),
    'course-other': lms.model.users.ServerUser(
        email = 'course-other@test.edulinq.org',
        id = '100030000',
        name = 'course-other',
    ),
    'course-owner': lms.model.users.ServerUser(
        email = 'course-owner@test.edulinq.org',
        id = '100040000',
        name = 'course-owner',
    ),
    'course-student': lms.model.users.ServerUser(
        email = 'course-student@test.edulinq.org',
        id = '100050000',
        name = 'course-student',
    ),
    'extra-course-student-1': lms.model.users.ServerUser(
        email = 'extra-course-student-1@test.edulinq.org',
        id = '100060000',
        name = 'extra-course-student-1',
    ),
    'extra-course-student-2': lms.model.users.ServerUser(
        email = 'extra-course-student-2@test.edulinq.org',
        id = '100070000',
        name = 'extra-course-student-2',
    ),
    'extra-course-student-3': lms.model.users.ServerUser(
        email = 'extra-course-student-3@test.edulinq.org',
        id = '100080000',
        name = 'extra-course-student-3',
    ),
    'extra-course-student-4': lms.model.users.ServerUser(
        email = 'extra-course-student-4@test.edulinq.org',
        id = '100090000',
        name = 'extra-course-student-4',
    ),
    'sevrer-admin': lms.model.users.ServerUser(
        email = 'server-admin@test.edulinq.org',
        id = '100100000',
        name = 'server-admin',
    ),
    'sevrer-creator': lms.model.users.ServerUser(
        email = 'server-creator@test.edulinq.org',
        id = '100110000',
        name = 'server-creator',
    ),
    'sevrer-owner': lms.model.users.ServerUser(
        email = 'server-owner@test.edulinq.org',
        id = '100120000',
        name = 'server-owner',
    ),
    'sevrer-user': lms.model.users.ServerUser(
        email = 'server-user@test.edulinq.org',
        id = '100130000',
        name = 'server-user',
    ),
}
