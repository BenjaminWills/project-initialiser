from initialise_project_utilites import (
    parse_json_content,
    create_dirs,
    create_files,
    load_premade_file,
)


def structure_project_using_json(path_to_template_json: str):
    json_contents = parse_json_content(path_to_template_json)
    directories = json_contents.get("directories", [])
    files = json_contents.get("files", [])
    create_dirs(directories)
    create_files(files)
    load_premade_file(json_contents)
