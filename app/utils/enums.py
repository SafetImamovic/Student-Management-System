from enum import Enum


class ErrorType(str, Enum):
    VALUE_ERROR = "value_error"
    TYPE_ERROR = "type_error"


class Location(str, Enum):
    BODY = "body"
    QUERY = "query"
    PATH = "path"
