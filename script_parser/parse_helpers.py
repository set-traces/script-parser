import re


class ReMatcher:
    def __init__(self, regex: str):
        self.compiled_re = re.compile(regex)

    def __call__(self, string: str, *args):
        match = self.compiled_re.search(string)
        return match