from dataclasses import dataclass
from typing import Dict, List, TypedDict, Union

LineType = str
ManuscriptLine = Dict[str, any]
ManuscriptLines = List[ManuscriptLine]


@dataclass(frozen=True)
class ManuscriptBody:
    lines: ManuscriptLines


FieldName = str
HeaderFieldValue = Union[str, Dict[FieldName, str]]
ManuscriptHeader = Dict[FieldName, any]


@dataclass(frozen=True)
class Manuscript:
    header: ManuscriptHeader
    body: ManuscriptBody
