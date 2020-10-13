import dataclasses
import json
import os

from pkg_resources import resource_stream

from script_parser.html_generator.html_generator import open_html
from script_parser.manuscript_parser import parse
from script_parser.manuscript_sound import read_aloud
from script_parser.parse_rules.parse_rules_ar21.parse_rules_ar21 import parse_rules as parse_rules_ar21
import sys

from script_parser.pdf_generator.pdf_generator import generate_pdf

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) < 1:
        print("args: filename | 'test'")
        exit()
    filename = args[0]

    if filename == 'test':
        manuscript_file = resource_stream("script_parser", "resources/Lærer på fest.txt")
        manuscript_raw = manuscript_file.read_aloud().decode("utf-8")
        manuscript_file.close()
    else:
        path = os.path.abspath(filename)
        with open(path, 'r') as f:
            manuscript_raw = f.buffer.read().decode('utf-8')

    manuscript = parse(manuscript_raw, parse_rules_ar21)

    class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)
    j = json.dumps(manuscript, indent=4, ensure_ascii=False, cls=EnhancedJSONEncoder)
    print(j)

    # read_aloud(manuscript)
    open_html(manuscript)
    generate_pdf(manuscript, "temp.pdf")
