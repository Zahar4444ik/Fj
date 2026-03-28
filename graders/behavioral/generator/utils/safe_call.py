import sys


def safe_call(func, arg, max_depth=1000):
    old_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(max_depth)
    try:
        return func(arg)
    except RecursionError:
        return None   # special value = non-terminating
    finally:
        sys.setrecursionlimit(old_limit)
