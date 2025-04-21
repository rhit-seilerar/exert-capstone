RUN_PLUGIN_TESTS = False
DEBUG_LEVEL = 0

def dprint(level: float, *args: object):
    if level <= DEBUG_LEVEL:
        print(*args)
