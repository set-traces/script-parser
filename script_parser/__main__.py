import dataclasses
import json
import os
import re

from pkg_resources import resource_stream

from script_parser.html_generator.html_generator import open_html
from script_parser.manuscript_parser import parse
from script_parser.manuscript_sound import read_aloud
from script_parser.parse_rules.parse_rules_ar21.parse_rules_ar21 import parse_rules as parse_rules_ar21
import sys

from script_parser.pdf_generator.pdf_generator import generate_pdf

help = """
Generate a json representation of a revue manuscript in output/<filename>.json

Usage:
  args: <filename> | 'test', [options...]
  if 'test' is given as the first argument, an example script will be parsed
  options:
    -w  generate html (output/<filename>.html)
    -p  generate pdf (output/<filename>.pdf)
    -v  generate text-to-speech and play it (output/<filename>.mp3)
"""

if __name__ == '__main__':
    args = sys.argv[1:]
    input_filename = args[0] if len(args) > 0 and not args[0].startswith('-') else None
    options = [arg for arg in args if arg.startswith('-')]

    if not input_filename or any(o in options for o in ['-h', '--help']):
        print(help)
        exit()

    if input_filename == 'test':
        file_path = 'Lærer på fest.txt'
        manuscript_file = resource_stream("script_parser", f"resources/{file_path}")
        manuscript_raw = manuscript_file.read().decode("utf-8")
        manuscript_file.close()
    else:
        file_path = input_filename
        path = os.path.abspath(file_path)
        with open(path, 'r') as f:
            manuscript_raw = f.buffer.read().decode('utf-8')

    manuscript = parse(manuscript_raw, parse_rules_ar21)

    filename = os.path.basename(file_path)
    filename_no_extension = re.fullmatch(r'(.*?)\..*$', filename).group(1)
    json_output_path = os.path.abspath(f'output/{filename_no_extension}.json')

    if not os.path.exists(os.path.dirname(json_output_path)):
        os.makedirs(os.path.dirname(json_output_path))


    class EnhancedJSONEncoder(json.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)
    with open(json_output_path, 'w+', encoding='utf-8') as fp:
        j = json.dump(manuscript, fp, indent=4, ensure_ascii=False, cls=EnhancedJSONEncoder)

    if '-v' in options:
        voice_path = os.path.abspath(f'output/{filename_no_extension}.mp3')
        read_aloud(manuscript, voice_path)

    if '-w' in options:
        html_path = os.path.abspath(f'output/{filename_no_extension}.html')
        open_html(manuscript, html_path)

    if '-p' in options:
        pdf_path = os.path.abspath(f'output/{filename_no_extension}.pdf')
        generate_pdf(manuscript, pdf_path)
