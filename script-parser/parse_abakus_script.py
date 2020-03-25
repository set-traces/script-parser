from enum import IntEnum, Enum
import json
from docx import Document
import uuid
from os import listdir
from os.path import isfile, join


def parse(filePath):
    CONTEXT_TOKEN = "Kontekst:"
    CHARCTERS_TOKEN = "Karakterer:"


    class States(Enum):
        BEGIN = "BEGIN"
        CONTEXT = "CONTEXT"
        ROLES = "ROLES"
        RANDOM_META = "RANDOM_META"
        SCRIPT = "SCRIPT"

    state = States.BEGIN

    title = []
    context = []
    rolesMeta = []
    random_lines = []
    lines = []

    def get_roles():
        return [
            role_meta["role"]
            for role_meta in rolesMeta
        ]

    def check_line_start_with_role_format(rawLine):
        return ":" in rawLine

    def check_line_start_with_role(rawLine):
        if ":" in rawLine:
            raw_role = rawLine.split(":")[0].strip()
            return raw_role in [
                role_meta["role"]
                for role_meta in rolesMeta
            ]

    def get_role_and_text(rawLine):
        if check_line_start_with_role(rawLine):
            return rawLine.split(":", maxsplit=1)
        else:
            return "", rawLine

    def parse_roles_in_text(text):
        return [
            role
            for role in get_roles()
            if role.lower() in text.lower()
        ]

    def state_begin(raw_line):
        if raw_line.startswith(CONTEXT_TOKEN):
            return States.CONTEXT, raw_line[len(CONTEXT_TOKEN):]
        else:
            title.append(raw_line.strip())
            return States.BEGIN, ""


    def state_context(raw_line):
        if raw_line.startswith(CHARCTERS_TOKEN):
            return States.ROLES, raw_line[len(CHARCTERS_TOKEN):]
        context.append(raw_line.strip())
        return States.CONTEXT, ""


    def state_roles(raw_line):
        if check_line_start_with_role_format(raw_line):
            role, description = raw_line.split(":")
            roleMeta = {
                "role": role.strip(),
                "description": description.strip(),
                "actor": None
            }
            rolesMeta.append(roleMeta)
            return States.ROLES, ""
        else:
            return States.RANDOM_META, raw_line

    def state_random_meta(raw_line):
        if raw_line.startswith(CONTEXT_TOKEN):
            return States.CONTEXT, raw_line[len(CONTEXT_TOKEN):]
        if raw_line.startswith(CHARCTERS_TOKEN):
            return States.ROLES, raw_line[len(CHARCTERS_TOKEN):]
        if check_line_start_with_role(raw_line) or raw_line.startswith("["):
            return States.SCRIPT, raw_line

        random_lines.append(raw_line.strip())
        return States.RANDOM_META, ""

    def state_script(raw_line):
        if "[" in raw_line:
            # an action
            if "]" in raw_line:
                action = raw_line[raw_line.index("[") + 1: raw_line.index("]")].strip()
            else:
                action = raw_line[raw_line.index("[") + 1:].strip()

            action_line = {
                "type": "ACTION",
                "roles": parse_roles_in_text(action),
                "text": action
            }
            lines.append(action_line)
            return States.SCRIPT, ""

        if check_line_start_with_role(raw_line):
            # a remark
            role, text = get_role_and_text(raw_line)
            line = {
                "type": "REMARK",
                "role": role.strip(),
                "text": text.strip()
            }
            lines.append(line)
            return States.SCRIPT, ""

        return States.RANDOM_META, raw_line

    state_funcs = {
        States.BEGIN: state_begin,
        States.CONTEXT: state_context,
        States.ROLES: state_roles,
        States.RANDOM_META: state_random_meta,
        States.SCRIPT: state_script
    }

    def serialize():
        serialized_script = {
            "id": uuid.uuid4().__str__(),
            "name": " ".join(title),
            "type": "SKETCH",
            "description": " ".join(context),
            "rolesMeta": rolesMeta,
            "randomLines": random_lines,
            "lines": lines
        }
        return serialized_script

    try:
        doc = Document(filePath)
    except:
        return serialize()


    # strip parapraphs
    paragraphs = [
        para.text.strip()
        for para in doc.paragraphs
    ]

    # remove empty paragraphs
    paragraphs = [
        text
        for text in paragraphs if text
    ]

    if len(paragraphs) == 0:
        return serialize()

    curr_paragraph_index = 0
    curr_line = paragraphs[curr_paragraph_index]

    while True:
        state_func = state_funcs[state]
        state, remaining_line = state_func(curr_line)

        if remaining_line != "":
            curr_line = remaining_line
        else:
            curr_paragraph_index += 1
            if curr_paragraph_index < len(paragraphs):
                curr_line = paragraphs[curr_paragraph_index]
            else:
                break

    return serialize()

def convert_script(load_path, save_path):
    parsed = parse(load_path)
    print("PARSED! " + load_path)
    file = open(save_path, "w")
    json.dump(parsed, file)
    file.close()

def convert_all_scripts_in_folder_to_one(load_path, save_path):
    load_files = [f for f in listdir(load_path) if isfile(join(load_path, f))]
    scripts = []
    for file in load_files:
        load_file_path = join(load_path, file)
        scripts.append(parse(load_file_path))
    file = open(save_path, "w")
    json.dump(scripts, file)
    file.close()

def convert_all_scripts_in_folder(path, save_path):
    load_files = [f for f in listdir(path) if isfile(join(path, f))]
    for file in load_files:
        load_file_path = join(path, file)
        save_file_path = join(save_path, file.split(".")[0] + ".json")
        print("Loading: " + load_file_path + "\n\tsaving to: " + save_file_path)

        convert_script(load_file_path, save_file_path)


convert_all_scripts_in_folder_to_one("example_scripts/satte_spor_sketsjer_ferdig", "example_scripts/satte_spor_sketsjer_ferdig/parsed/all.json")



# print(parse("example_scripts/satte_spor_sketsjer_ferdig/Abakus_ nye organisasjonskart.docx"))