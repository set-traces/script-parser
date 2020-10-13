import re
from typing import List


def header_field_characters_parser(characters_raw: List[List[str]]):
    matcher = re.compile(r"""
        ^ \s*
        (?P<name> .*?)                  # character name
        \s* ( \((?P<alias> .*?)\) )?    # optional alias in parentheses
        : \s* (?P<description> .*)      # character description
        $
    """, re.VERBOSE)

    def parse_char(char_raw: str):
        match = matcher.fullmatch(char_raw)
        if match:
            parsed_char = {
                field: value
                for field, value in match.groupdict().items()
            }
            return parsed_char
        else:
            return {
                'invalid': True,
                'raw': char_raw
            }

    if not isinstance(characters_raw, list) or len(characters_raw) == 0 or not isinstance(characters_raw[0], list):
        return []

    characters = characters_raw[0]
    parsed_characters = [
        parse_char(char)
        for char in characters
    ]
    return {
        'list': parsed_characters,
        'notes': ''
    }
