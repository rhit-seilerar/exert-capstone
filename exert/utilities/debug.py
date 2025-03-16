RUN_PLUGIN_TESTS = True
DEBUG_LEVEL = 1

def dprint(level, *args): # pragma: no cover
    if level <= DEBUG_LEVEL:
        print(*args)
