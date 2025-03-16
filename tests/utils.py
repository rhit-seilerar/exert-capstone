def expect_error(func, error = AssertionError):
    try:
        func()
        assert False
    except error:
        pass
