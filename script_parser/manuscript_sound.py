from script_parser.manuscript_types import Manuscript
from gtts import gTTS
import os

def read_aloud(manuscript: Manuscript):
    characters = [char for char in manuscript.header['characters']['list'] if not char.get('invalid')]
    langs = ['no', 'sv', 'da', 'fi', 'nl', 'de']
    lang_by_char_name = {
        char['name']: langs[i % len(langs)]
        for i, char in enumerate(characters)
    }

    def mapping(line):
        if line['type'] == 'remark':
            return line['remark'], lang_by_char_name[line['character']]
        elif line['type'] == 'action':
            return line['action'], 'en'

    lines_text_with_lang = [
        mapping(line)
        for line in manuscript.body.lines
        if 'type' in line and line['type'] in ['remark', 'action']
    ]

    voice_objs = [
        gTTS(text=line, lang=lang)
        for line, lang in lines_text_with_lang
    ]

    with open('temp_voice.mp3', 'wb') as fp:
        for voice_obj in voice_objs:
            voice_obj.write_to_fp(fp)

    os.system("temp_voice.mp3")


