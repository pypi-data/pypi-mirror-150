import re
import sys
from .base import *


class ExactMatcher(BaseMatcher):
    def __init__(self):
        self.regex = r'^{}$'.format(SEMVER_PATTERN)
    
    def match_version(self, version_string):
        version_pairs = self._get_matched_version(version_string)

        if version_pairs is None:
            return NoMatch

        wanted_version = [t[0] for t in version_pairs]
        for wanted, actual in version_pairs:
            if wanted is not None and int(wanted) != actual:
                mapped_version_string = '.'.join('x' if m is None else m for m in wanted_version)
                return WrongVersion(mapped_version_string)

        return OkVersion(wanted_version)