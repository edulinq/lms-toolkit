import lms.api.assignment.testing

GRADEBOOK_ASSIGNMENTS = {
    "67890": lms.api.assignment.testing.ASSIGNMENTS['67890'] | {
        "count": 2,
    },
    "67891": lms.api.assignment.testing.ASSIGNMENTS['67891'] | {
        "count": 2,
    },
    "67892": lms.api.assignment.testing.ASSIGNMENTS['67892'] | {
        "count": 0,
    }
}

GRADEBOOK_GRADES = {
    "aalvarez@ucsc.edu": {
        "67890": 1.0,
        "67891": 1.0
    },
    "bburnquist@ucsc.edu": {
        "67890": 0.5,
        "67891": 1.0
    }
}
