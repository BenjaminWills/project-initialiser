import os
import argparse
from typing import List, Dict
import json


class Initalise_repository:
    """
    A class that will build a repository structure based on an input json file.
    """

    @staticmethod
    def _directory_error_message(directory_path: str):
        print(
            f"""
            {'-'*100}
            \t Directory {directory_path} already exists
            {'-'*100}
            """
        )

    @staticmethod
    def _directory_success_message(directory_path: str):
        print(
            f"""
            {'-'*100}
            \t Directory {directory_path} successfully created
            {'-'*100}
            """
        )

    @staticmethod
    def _file_error_message(full_file_path: str):
        print(
            f"""
            {'-'*100}
            \t File {full_file_path} already exists
            {'-'*100}
            """
        )

    @staticmethod
    def _file_success_message(full_file_path: str):
        print(
            f"""
            {'-'*100}
            \t File {full_file_path} successfully created
            {'-'*100}
            """
        )

    @staticmethod
    def get_dir_path(file_path: str) -> str:
        return f"{os.getcwd()}/{file_path}"

    @staticmethod
    def mkdir_if_not_exists(file_path: str):
        directory_path = Initalise_repository.get_dir_path(file_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            Initalise_repository._directory_success_message(directory_path)
        else:
            Initalise_repository._directory_error_message(directory_path)

    @staticmethod
    def mkfile_if_not_exists(file_path: str):
        full_file_path = Initalise_repository.get_dir_path(file_path)
        if not os.path.exists(full_file_path):
            with open(full_file_path, "w"):
                Initalise_repository._file_success_message(full_file_path)
        else:
            Initalise_repository._file_error_message(full_file_path)

    @staticmethod
    def parse_json_content(path_to_template_json: str) -> Dict[str, str]:
        try:
            with open(path_to_template_json, "r") as json_file:
                json_object = json.load(json_file)
            return json_object
        except:
            print("JSON file could not be parsed.")

    @staticmethod
    def create_dirs(directories: List[str]):
        if directories:
            for path in directories:
                Initalise_repository.mkdir_if_not_exists(path)

    @staticmethod
    def create_files(files: List[str]):
        if files:
            for path in files:
                Initalise_repository.mkfile_if_not_exists(path)

    @staticmethod
    def structure_project_using_json(path_to_template_json: str):
        json_contents = Initalise_repository.parse_json_content(path_to_template_json)
        directories = json_contents.get("directories", [])
        files = json_contents.get("files", [])
        Initalise_repository.create_dirs(directories)
        Initalise_repository.create_files(files)

    @staticmethod
    def clean_directory(path_to_template_json: str):
        json_contents = Initalise_repository.parse_json_content(path_to_template_json)
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


parser = argparse.ArgumentParser(
    prog="Directory initialiser",
    description="Initialise project with JSON config file or command line arguments",
    epilog="Project directories initialised",
)
parser.add_argument(
    "--initialise",
    type=Initalise_repository.structure_project_using_json,
    help="""
    Initialises the project, using a JSON as a structure:
        \n - Directories
        \n - Files
    """,
)
parser.add_argument(
    "--clean_directory",
    type=Initalise_repository.clean_directory,
    help="""
    Will remove all files specified in the structure JSON file:
        \n - Directories
        \n - Files
    """,
)

args = parser.parse_args()
