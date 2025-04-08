from typing import Any
def expect_error(func: Any, error: type[AssertionError] = AssertionError):
    try:
        func()
        assert False
    except error:
        pass
