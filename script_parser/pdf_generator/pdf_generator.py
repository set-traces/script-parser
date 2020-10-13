import pdfkit

from script_parser.html_generator.html_generator import generate_html
from script_parser.manuscript_types import Manuscript


def generate_pdf(manuscript: Manuscript, filename: str):
    html = generate_html(manuscript)
    options = {
        'page-size': 'A4',
        'dpi': '300',
        'margin-top': '10mm',
        'margin-right': '0mm',
        'margin-bottom': '10mm',
        'margin-left': '0mm',
        'encoding': "UTF-8",
        'no-outline': None
    }
    pdfkit.from_string(html, filename, options=options)
