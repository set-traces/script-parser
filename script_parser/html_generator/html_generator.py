import os
import webbrowser
from typing import Union

from pkg_resources import resource_stream

from script_parser.manuscript_types import Manuscript
from jinja2 import Template


def generate_html(manuscript: Manuscript) -> str:
    html_file = resource_stream("script_parser", "resources/html_generator/manuscript.j2")
    template = Template(html_file.read().decode("utf-8"))
    html_file.close()

    styles_file = resource_stream("script_parser", "resources/html_generator/styles.css")
    styles = styles_file.read().decode("utf-8")
    styles_file.close()

    colors = ['red', 'green', 'blue', 'aquamarine']
    characters = [char for char in manuscript.header['characters']['list'] if not char.get('invalid')]
    color_by_character = {
        char['name']: colors[i % len(colors)]
        for i, char in enumerate(characters)
    }

    html = template.render(
        styles=styles,
        title=manuscript.header['title'][0],
        manuscript_lines=manuscript.body.lines,
        character_color=color_by_character
    )
    return html


def save_html(manuscript_or_html: Union[Manuscript, str], save_path: str):
    if isinstance(manuscript_or_html, Manuscript):
        html = generate_html(manuscript_or_html)
    else:
        html = manuscript_or_html

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(html)


def open_html(manuscript_or_html: Union[Manuscript, str], save_path: str):
    save_html(manuscript_or_html, save_path)
    url = 'file://' + save_path
    webbrowser.open(url)
