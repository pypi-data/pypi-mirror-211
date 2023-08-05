import functools

def if_regex_return_group(group_number):
    def decorator_regex_return_group(fn):
        @functools.wraps(fn)
        def wrapper(value):
            regex_test = fn(value)

            return (
                regex_test.group(group_number) if
                regex_test else
                None)

        return wrapper
    return decorator_regex_return_group


def if_regex_return_value(fn):
    @functools.wraps(fn)
    def wrapper(value):
        regex_test = fn(value)
        if regex_test:
            return regex_test.group(0)
        else:
            return None
    return wrapper