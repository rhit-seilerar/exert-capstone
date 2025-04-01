RUN_PLUGIN_TESTS = False
DEBUG_LEVEL = 2

def dprint(level, *args):
    if level <= DEBUG_LEVEL:
        print(*args)
