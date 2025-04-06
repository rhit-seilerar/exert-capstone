RUN_PLUGIN_TESTS = False
DEBUG_LEVEL = 0

def dprint(level: int, *args: tuple):
    if level <= DEBUG_LEVEL:
        print(*args)
