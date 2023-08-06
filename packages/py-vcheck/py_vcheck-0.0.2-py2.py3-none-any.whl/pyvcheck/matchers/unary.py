from .exact import ExactMatcher
from .base import *


class UnaryMatcher(BaseMatcher):
    def __init__(self, op, comparator):
        self.regex = r'^\s*{}{}$'.format(op, SEMVER_PATTERN)
        self._comp = comparator
    
    def match_version(self, version_string):
        version_pairs = self._get_matched_version(version_string)

        if version_pairs is None:
            return NoMatch

        wanted_version = [t[0] for t in version_pairs]
        for wanted, actual in version_pairs:
            if wanted is not None and self._comp(actual, int(wanted)) == False:
                mapped_version_string = '.'.join('x' if m is None else m for m in wanted_version)
                return WrongVersion('at most {}'.format(mapped_version_string))

        return OkVersion(wanted_version)


LessThanMatcher = UnaryMatcher(r'\<', lambda a, b: a < b)
GreaterThanMatcher = UnaryMatcher(r'\>', lambda a, b: a > b)
LessThanEqualMatcher = UnaryMatcher(r'\<=', lambda a, b: a <= b)
GreaterThanEqualMatcher = UnaryMatcher(r'\>=', lambda a, b: a >= b)