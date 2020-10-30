import functools


def method_decorator(decorator):
    """
    Utility for decorators which access positional arguments of original functions to be used on class methods.
    """

    def new_decorator(f):
        @functools.wraps(f)
        def func(self, *args, **kwargs):
            return decorator(functools.partial(f, self))(*args, **kwargs)

        return func

    return new_decorator
