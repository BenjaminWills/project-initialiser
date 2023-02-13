import os
import json
import itertools

from s3_utilities import S3
from typing import List, Dict


def directory_error_message(directory_path: str):
    print(
        f"""
        {'-'*100}
        \t Directory {directory_path} already exists
        {'-'*100}
        """
    )


def directory_success_message(directory_path: str):
    print(
        f"""
        {'-'*100}
        \t Directory {directory_path} successfully created
        {'-'*100}
        """
    )


def file_error_message(full_file_path: str):
    print(
        f"""
        {'-'*100}
        \t File {full_file_path} already exists
        {'-'*100}
        """
    )


def file_success_message(full_file_path: str):
    print(
        f"""
        {'-'*100}
        \t File {full_file_path} successfully created
        {'-'*100}
        """
    )


def get_dir_path(file_path: str) -> str:
    return f"{os.getcwd()}/{file_path}"


def mkdir_if_not_exists(file_path: str):
    directory_path = get_dir_path(file_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
        directory_success_message(directory_path)
    else:
        directory_error_message(directory_path)


def mkfile_if_not_exists(file_path: str):
    full_file_path = get_dir_path(file_path)
    if not os.path.exists(full_file_path):
        with open(full_file_path, "w"):
            file_success_message(full_file_path)
    else:
        file_error_message(full_file_path)


def parse_json_content(path_to_template_json: str) -> Dict[str, str]:
    try:
        with open(path_to_template_json, "r") as json_file:
            json_object = json.load(json_file)
        return json_object
    except:
        print("JSON file could not be parsed.")


def create_dirs(directories: List[str]):
    if directories:
        for path in directories:
            mkdir_if_not_exists(path)


def create_files(files: List[str]):
    if files:
        for path in files:
            mkfile_if_not_exists(path)


def load_premade_file(loaded_json: Dict[str, str]):
    # A function to load a premade file, such as a python .gitignore or a sample readme into a project
    s3 = S3(region_name="eu-west-2")
    if loaded_json.get(".gitignore", False):
        s3.download_object("projectinitialiserbucket", ".gitignore", "./.gitignore")


def include_directory_in_path(file_path: str, root: str) -> str:
    return os.path.join(root, file_path)


def flatten_list(input_list: list) -> list:
    return list(itertools.chain(*input_list))


def get_dirs_and_files() -> Dict[str, List[str]]:
    files_master = []
    dirs_master = []

    for root, dirs, files in os.walk("."):
        files = [
            include_directory_in_path(file_path=f, root=root)
            for f in files
            if not f[0] == "."  # Dont include hidden directories
        ]
        dirs[:] = [
            d for d in dirs if not d[0] == "."
        ]  # Dont incluse hidden directories

        if files:  # If there are files to append
            files_master.append(files)
        if dirs:  # If there are files to append
            dirs_master.append(dirs)

    return {
        "files": flatten_list(files_master),
        "directories": flatten_list(dirs_master),
    }
