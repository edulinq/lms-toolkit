import lms.model.users

# {course_id: {email: user, ...}, ...}
COURSE_USERS = {
    '1': {
        'course-admin@test.edulinq.org': lms.model.users.CourseUser(
            email = 'course-admin@test.edulinq.org',
            id = '2',
            name = 'course-admin',
            username = 'course-admin@test.edulinq.org',
            role = 'TaEnrollment',
        ),
        'course-grader@test.edulinq.org': lms.model.users.CourseUser(
            email = 'course-grader@test.edulinq.org',
            id = '3',
            name = 'course-grader',
            username = 'course-grader@test.edulinq.org',
            role = 'TaEnrollment',
        ),
        'course-other@test.edulinq.org': lms.model.users.CourseUser(
            email = 'course-other@test.edulinq.org',
            id = '4',
            name = 'course-other',
            username = 'course-other@test.edulinq.org',
            role = 'ObserverEnrollment',
        ),
        'course-owner@test.edulinq.org': lms.model.users.CourseUser(
            email = 'course-owner@test.edulinq.org',
            id = '5',
            name = 'course-owner',
            username = 'course-owner@test.edulinq.org',
            role = 'TeacherEnrollment',
        ),
        'course-student@test.edulinq.org': lms.model.users.CourseUser(
            email = 'course-student@test.edulinq.org',
            id = '6',
            name = 'course-student',
            username = 'course-student@test.edulinq.org',
            role = 'StudentEnrollment',
        ),
    },
}
