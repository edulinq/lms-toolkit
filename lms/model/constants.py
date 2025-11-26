import typing

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

OUTPUT_FORMAT_JSON: str = 'json'
OUTPUT_FORMAT_TABLE: str = 'table'
OUTPUT_FORMAT_TEXT: str = 'text'

OUTPUT_FORMATS: typing.List[str] = [
    OUTPUT_FORMAT_JSON,
    OUTPUT_FORMAT_TABLE,
    OUTPUT_FORMAT_TEXT,
]
