# script-parser

This is a manuscript parser for Abakusrevyen 2021.

The parser is flexible to easily allow different script syntaxes.

The script can also generate a pretty html, pdf and text-to-speach

## Getting started

### Prerequisits
* [pipenv](https://pypi.org/project/pipenv/)
* Python 3.7^

### Installation
1. Clone the repo
```
git clone https://github.com/set-traces/script-parser.git
```
or
```
git clone git@github.com:set-traces/script-parser.git
```
2. Navigate to the root folder
3. Intall python packages
```
pipenv install
```
4. to test if it works, run
```
pipenv run python -m script_parser test
```
This will parse a test manuscript

### Usage
```
args: <filename> | 'test', [options...]
if 'test' is given as the first argument, an example script will be parsed

options:
  -w  generate html (output/<filename>.html)
  -p  generate pdf (output/<filename>.pdf)
  -v  generate text-to-speech and play it (output/<filename>.mp3)
```
## Input / output structure

The putput json has the following structure:
manuscript:
  header:
    [header_field: value]
  body:
    lines:
      [line]

where header fields and values as well as line data is provided by parser rules for a given manuscript syntax.

The currently supported syntax is `ar21`, based on scripts from Abakusrevyen 2021 (not songs as of now)
The header ends with at least 5 "-" or "_".
The manuscript ends with at least 5 "-" or "_" or the end of the file.

The header fields are given as follows
- title: first line
- context: Starts with "Kontekst:"
- characters: Starts with "Karakterer:"
- costume: Starts with "Kostyme:"
- technicians: Starts with "Teknikk:"
- props: Starts with "Rekvisitter:"
- band: Starts with "Band:"
- dance: Starts with "Dans:"
- choir: Start with "Kor:"

The lines are as follows:
- remark: {type: "remark", remark: str, character: str}, given by a line starting with a character from the header "character" field
- action: {type: "action", action: str}, given by a line surounded by "[]"
- comment: {type: "comment", comment: str}, given by a line starting with "//"
- invalid: {invalid: true, raw: str}, given by a line not corresponding to the above.
