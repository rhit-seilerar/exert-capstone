from collections.abc import Callable
from typing import Any

def expect_error(func: Callable[[], Any], error: type[Exception] = AssertionError) -> None:
    try:
        func()
        assert False
    except error:
        pass
