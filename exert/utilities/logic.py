from typing import Callable, Optional

class OrElse[T]:
    def __call__(self, value: Optional[T], default: T | Callable[[], T]) -> T:
        if value is not None:
            return value
        if callable(default):
            return default()
        return default
