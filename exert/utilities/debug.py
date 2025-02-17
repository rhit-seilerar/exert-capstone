DEBUG_LEVEL = 3

def dprint(level, *args):
    if level <= DEBUG_LEVEL:
        print(*args)
