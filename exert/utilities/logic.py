from typing import TypeVar, Callable

T = TypeVar('T')
def or_else(value: T | None, default: T | Callable[[], T]) -> T:
    return (default() if callable(default) else default) if value is None else value
