from typing import Optional

from script_parser.manuscript_types import ManuscriptHeader


def ar_named_header_field_re(*fields: str):
    fields_as_re_groups = (f"({field})" for field in fields)
    fields_set_re = "|".join(fields_as_re_groups)
    return r'(?mi)^\s*{}:'.format(fields_set_re)


def characters_set_re(header: ManuscriptHeader):
    characters_field = header['characters']
    if characters_field is None or not isinstance(characters_field, dict):
        raise ValueError("characters must be present and be a dict to parse lines")

    if 'list' not in characters_field:
        raise ValueError("character list not present")
    character_list = characters_field['list']

    valid_character_list = [char for char in character_list if 'invalid' not in char]

    character_names = [char['name'] for char in valid_character_list]
    character_aliases = [char['alias'] for char in valid_character_list if 'alias' in char]

    characters_matches = character_names + character_aliases
    fields_set_re = "|".join((f"({char})" for char in characters_matches))
    return fields_set_re


def get_name_of_alias(header: ManuscriptHeader, alias: str) -> Optional[str]:
    characters_field = header['characters']
    characters = characters_field['list']
    character_with_alias = next((char for char in characters if 'alias' in char and char['alias'] == alias), None)
    return character_with_alias['name'] if character_with_alias is not None else None
