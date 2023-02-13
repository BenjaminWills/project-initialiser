import os

from initialise_project_utilites import parse_json_content


def clean_directory(path_to_template_json: str):
    json_contents = parse_json_content(path_to_template_json)
    directories = json_contents.get("directories", [])
    files = json_contents.get("files", [])
    for file in files:
        try:
            os.remove(file)
        except:
            pass
    for directory in directories:
        try:
            os.removedirs(directory)
        except:
            pass
