import re
import sys
from ..exceptions import VersionError


class MatcherResult:
    pass


NoMatch = MatcherResult()


class WrongVersion(MatcherResult):
    def __init__(self, expected):
        self._expected = expected

    def raise_exception(self):
        raise VersionError(
            "Expected version {}, got {} instead"
            .format(self._expected, sys.version))


class OkVersion(MatcherResult):
    def __init__(self, version):
        self.version = version


class BaseMatcher:
    def _get_matched_version(self, version_string):
        if self.regex is None:
            raise NotImplementedError("Implement me!")

        exact_version_regex = self.regex

        m = re.search(exact_version_regex, version_string, re.M)
        if m is None:
            return None

        groups = m.groups()
        selectors = [0, 2, 4]
        python_version = sys.version_info[:3]
        wanted_version = [groups[i] for i in selectors]

        return list(zip(wanted_version, python_version))

    def match_version(self, version_string):
        raise NotImplementedError("Implement me!")


SEMVER_PATTERN = r'\s*([0-9]+)(\.([0-9]+))?(\.([0-9]+))?\s*'