import enum
import typing

# TEST - Make enum.
BACKEND_TYPE_BLACKBOARD: str = 'blackboard'
BACKEND_TYPE_CANVAS: str = 'canvas'
BACKEND_TYPE_MOODLE: str = 'moodle'

BACKEND_TYPES: typing.List[str] = [
    BACKEND_TYPE_BLACKBOARD,
    BACKEND_TYPE_CANVAS,
    BACKEND_TYPE_MOODLE,
]

HEADER_KEY_BACKEND: str = 'edq-lms-backend'
HEADER_KEY_WRITE: str = 'edq-lms-write'

class OutputFormat(enum.Enum):
    """ Different formats that are available for output. """

    JSON = 'json'
    TABLE = 'table'
    TEXT = 'text'
