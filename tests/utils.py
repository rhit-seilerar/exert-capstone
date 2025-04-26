from collections.abc import Callable

def expect_error(func: Callable[[], None], error: type[Exception] = AssertionError) -> None:
    try:
        func()
        assert False
    except error:
        pass
