import json

from initialise_project_utilites import get_dirs_and_files


def save_repository(output_path: str):
    with open(output_path, "w") as output:
        output.write(json.dumps(get_dirs_and_files()))
