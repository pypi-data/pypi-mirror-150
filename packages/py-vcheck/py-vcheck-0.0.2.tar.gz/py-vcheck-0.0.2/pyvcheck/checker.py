import sys
from pyvcheck.matchers import *


MATCHERS = [
    ExactMatcher(),
    LessThanMatcher,
    GreaterThanMatcher,
    LessThanEqualMatcher,
    GreaterThanEqualMatcher
]


def version(version_string):
    def wrapper(func):
        def func_wrapper(*args, **kwargs):
            for matcher in MATCHERS:
                result = matcher.match_version(version_string)

                if isinstance(result, WrongVersion):
                    result.raise_exception()
                elif isinstance(result, OkVersion):
                    return func(*args, **kwargs)

            raise ValueError("Invalid value passed to version: {}".format(version_string))

        return func_wrapper

    return wrapper    