from typing import Any
def expect_error(func: Any, error: Any = AssertionError):
    try:
        func()
        assert False
    except error:
        pass
