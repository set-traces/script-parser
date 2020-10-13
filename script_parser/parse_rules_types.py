from dataclasses import dataclass
from typing import Dict, Optional, Callable, List

from script_parser.manuscript_types import ManuscriptHeader, FieldName, LineType

Re = str
ReTemplate = str

MatchObject = any
Matcher = Callable[[str, ManuscriptHeader], Optional[MatchObject]]
MatchConsumer = Callable[[MatchObject, Optional[ManuscriptHeader]], any]


@dataclass(frozen=True)
class HeaderField:
    start_re: str
    end_re: Optional[str] = None
    convert: Optional[Callable[[List[any]], any]] = None


@dataclass(frozen=True)
class ManuscriptHeaderRules:
    field_rules: Dict[FieldName, HeaderField]
    end_re: Optional[Re]


@dataclass(frozen=True)
class LineRetriever:
    matcher: Matcher
    convert: Dict[FieldName, MatchConsumer]


@dataclass(frozen=True)
class ManuscriptBodyRules:
    line_rules: Dict[LineType, LineRetriever]
    end_rule: Re


@dataclass(frozen=True)
class ManuscriptRules:
    header_rules: ManuscriptHeaderRules
    body_rules: ManuscriptBodyRules


@dataclass(frozen=True)
class ParseRules:
    allow_multiple_scripts: bool
    manuscript_rules: ManuscriptRules

