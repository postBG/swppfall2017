import functools


def handle_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('Caught Exception: %s' % e)
    return wrapper
