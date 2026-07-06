import enum

SERVER_SLUG: str = '<edq-lms-backend-server>'

HEADER_KEY_BACKEND: str = 'edq-lms-backend'
HEADER_KEY_WRITE: str = 'edq-lms-write'

class BackendType(enum.Enum):
    """ The supported LMS backends. """

    BLACKBOARD = 'blackboard'
    CANVAS = 'canvas'
    MOODLE = 'moodle'

class OutputFormat(enum.Enum):
    """ Different formats that are available for output. """

    JSON = 'json'
    TABLE = 'table'
    TEXT = 'text'
