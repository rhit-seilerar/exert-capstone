from collections.abc import Callable

def expect_error(func: Callable[[], None], error = AssertionError):
    try:
        func()
        assert False
    except error:
        pass
