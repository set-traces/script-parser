import functools
from typing import Dict, Optional, List

from script_parser.manuscript_types import HeaderFieldValue, Manuscript, ManuscriptBody
from script_parser.parse_rules_types import ParseRules, HeaderField, ManuscriptHeaderRules, \
    ManuscriptBodyRules, LineRetriever, ManuscriptHeader, ManuscriptRules
import re


def parse_list(text: str) -> Optional[List[str]]:
    list_item_symb = "*"
    lines = text.split('\n')

    list_line_re = r'(?m)^\s*{}(.*)$'.format(re.escape(list_item_symb))
    list_line_matcher = re.compile(list_line_re)

    def construct_lines_reducer(lines_curr_list, line) -> (List[str], List[str]):
        (curr_lines, current_list) = lines_curr_list
        if match := list_line_matcher.match(line):
            return curr_lines, current_list + [match.group(1).strip()]
        else:
            clean_line = line.strip()
            if len(current_list) > 0:
                return curr_lines + [current_list, clean_line], []
            else:
                return curr_lines + [clean_line], current_list

    (lines_with_lists, last_list) = functools.reduce(
        construct_lines_reducer,
        lines,
        ([], [])
    )

    constructed_lines = lines_with_lists if len(last_list) == 0 else lines_with_lists + [last_list]
    return constructed_lines


def parse_manuscript_header(header_raw: str, header_rules: ManuscriptHeaderRules) -> Dict[str, HeaderFieldValue]:
    fields_start_matches = {
        field_name: match
        for field_name, field in header_rules.field_rules.items()
        if (match := re.search(field.start_re, header_raw)) is not None
    }

    fields_matches_by_start = [
        (match.span()[0], field_name, match)
        for field_name, match in fields_start_matches.items()
    ]

    fields_match_ordered = sorted(
        fields_matches_by_start,
        key=lambda elem: elem[0]
    )

    fields_match_span_by_name = {
        field_name: match.span()
        for (_, field_name, match) in fields_match_ordered
    }

    fields_content_span = {
        field_name: (span[1], next_span[0] if next_span is not None else None)
        for (field_name, span), next_span in zip(
            fields_match_span_by_name.items(),
            list(fields_match_span_by_name.values())[1:] + [None]
        )
    }

    fields_values_raw = {
        field_name: header_raw[start: end]
        for field_name, (start, end) in fields_content_span.items()
    }

    fields_values = {
        field_name: value.strip()
        for field_name, value in fields_values_raw.items()
    }

    list_expanded_field_values = {
        field_name: l if (l := parse_list(value)) else value
        for field_name, value in fields_values.items()
    }

    field_parsers = [
        field.convert
        for field in header_rules.field_rules.values()
    ]

    custom_parsed_field_values = {
        field_name: parser(value) if parser is not None else value
        for (field_name, value), parser in zip(list_expanded_field_values.items(), field_parsers)
    }
    return custom_parsed_field_values


def parse_manuscript_body(body_raw: str, body_rules: ManuscriptBodyRules, header: ManuscriptHeader):
    lines = [
        clean_line
        for line in body_raw.split('\n')
        if (clean_line := line.strip()) != ""
    ]

    def convert_line(line: str):
        line_retrievers: Dict[str, LineRetriever] = body_rules.line_rules
        matched_line = next((
            (line_type, match, retriever)
            for line_type, retriever in line_retrievers.items()
            if (match := retriever.matcher(line, header)) is not None and match is not False
        ), None)
        if matched_line:
            (line_type, match, retriever) = matched_line
            converted_line = {
                field: converter(match, header)
                for field, converter in retriever.convert.items()
            }
            return {**converted_line, 'type': line_type}
        else:
            return {
                'invalid': True,
                'raw': line
            }

    converted_lines = [
        converted_line
        for line in lines
        if (converted_line := convert_line(line)) is not None
    ]
    return ManuscriptBody(
        lines=converted_lines
    )


def extract_raw_header_body(manuscript_raw: str, manuscript_rules: ManuscriptRules) -> (str, str, str):
    header_end_match = re.search(manuscript_rules.header_rules.end_re, manuscript_raw)
    if not header_end_match:
        return ""
    header_end_index, body_start_index = header_end_match.span()
    header_raw: str = manuscript_raw[:header_end_index]
    no_header_raw = manuscript_raw[body_start_index:]
    body_end_match = re.search(manuscript_rules.body_rules.end_rule, no_header_raw)
    if body_end_match:
        (body_end_index, rest_start_index) = body_end_match.span()
        body_raw = no_header_raw[:body_end_index]
        rest_raw = no_header_raw[rest_start_index:]
    else:
        body_raw = no_header_raw
        rest_raw = ""
    return header_raw, body_raw, rest_raw


def parse(manuscript_raw: str, parse_rules: ParseRules) -> Manuscript:
    header_raw, body_raw, rest_raw = extract_raw_header_body(manuscript_raw, parse_rules.manuscript_rules)
    parsed_header = parse_manuscript_header(header_raw, parse_rules.manuscript_rules.header_rules)
    parsed_body = parse_manuscript_body(body_raw, parse_rules.manuscript_rules.body_rules, parsed_header)

    parsed_manuscript = Manuscript(
        header=parsed_header,
        body=parsed_body
    )

    return parsed_manuscript
