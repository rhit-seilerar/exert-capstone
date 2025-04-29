from typing import TypeVar

T = TypeVar('T')
def or_else(value: T, default: T) -> T:
    return default if value is None else value
