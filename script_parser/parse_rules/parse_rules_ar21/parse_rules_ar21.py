"""
Parse rules for the syntax used for script writing in Abakusrevyen 2021
"""

from script_parser.parse_helpers import ReMatcher
from script_parser.parse_rules.parse_rules_ar21.header_field_characters_parser import header_field_characters_parser
from script_parser.parse_rules.parse_rules_ar21.helpers import ar_named_header_field_re, characters_set_re, \
    get_name_of_alias
from script_parser.parse_rules_types import ParseRules, ManuscriptRules, HeaderField, ManuscriptHeaderRules, \
    ManuscriptBodyRules, LineRetriever

header_rules = ManuscriptHeaderRules(
    field_rules={
        'title': HeaderField(
            start_re=r'(?m)^',
            end_re=r'(?m)$',
        ),
        'context': HeaderField(
            start_re=ar_named_header_field_re("kontekst"),
        ),
        'characters': HeaderField(
            start_re=ar_named_header_field_re("karakterer"),
            convert=header_field_characters_parser
        ),
        'costume': HeaderField(
            start_re=ar_named_header_field_re("kostyme"),
        ),
        'technicians': HeaderField(
            start_re=ar_named_header_field_re("teknikk"),
        ),
        'props': HeaderField(
            start_re=ar_named_header_field_re("rekvisitter"),
        ),
        'band': HeaderField(
            start_re=ar_named_header_field_re("band"),
        ),
        'dance': HeaderField(
            start_re=ar_named_header_field_re("dans"),
        ),
        'choir': HeaderField(
            start_re=ar_named_header_field_re("kor"),
        ),
    },
    end_re=r'(?m)^\s*[_-]{5,}'
)

body_rules = ManuscriptBodyRules(
    line_rules={
        'comment': LineRetriever(
            matcher=ReMatcher(r'^\s*//(.*)\s*$'),
            convert={
                'comment': lambda m, _: m.group(1)
            }
        ),
        'action': LineRetriever(
            matcher=ReMatcher(r'^\s*\[(.*)\]\s*$'),
            convert={
                'action': lambda m, _: m.expand(r'\1')
            }
        ),
        'remark': LineRetriever(
            matcher=lambda line, header: ReMatcher(
                r'(?i)^\s*(?P<name>{}):\s*(?P<remark>.*?)\s*$'.format(characters_set_re(header)))(line),
            convert={
                'character': lambda m, header:
                    alias if (name := m.group("name")) and (alias := get_name_of_alias(header, name)) \
                    else name,
                'remark': lambda m, _: m.group("remark")
            }
        )
    },
    end_rule=r'(?m)^\s*[_-]{5,}'
)

parse_rules = ParseRules(
    allow_multiple_scripts=False,
    manuscript_rules=ManuscriptRules(
        header_rules=header_rules,
        body_rules=body_rules
    )
)
