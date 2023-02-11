import itertools
import os
import argparse
from typing import List, Dict
import json
from s3_utilities import S3


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
        Initalise_repository.load_premade_file(json_contents)

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

    @staticmethod
    def include_directory_in_path(file_path: str, root: str) -> str:
        return os.path.join(root, file_path)

    @staticmethod
    def flatten_list(input_list: list) -> list:
        return list(itertools.chain(*input_list))

    @staticmethod
    def get_dirs_and_files() -> Dict[str, List[str]]:
        files_master = []
        dirs_master = []

        for root, dirs, files in os.walk("."):
            files = [
                Initalise_repository.include_directory_in_path(file_path=f, root=root)
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
            "files": Initalise_repository.flatten_list(files_master),
            "directories": Initalise_repository.flatten_list(dirs_master),
        }

    @staticmethod
    def save_repository(output_path: str):
        with open(output_path, "w") as output:
            output.write(json.dumps(Initalise_repository.get_dirs_and_files()))

    @staticmethod
    def load_premade_file(loaded_json: Dict[str, str]):
        # A function to load a premade file, such as a python .gitignore or a sample readme into a project
        if loaded_json.get(".gitignore", False):
            s3 = S3(region_name="eu-west-2")
            s3.download_object("projectinitialiserbucket", ".gitignore", "./.gitignore")


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
parser.add_argument(
    "--save_directory",
    type=Initalise_repository.save_repository,
    help="""
    Will save all files specified in the structure JSON file:
        \n - Directories
        \n - Files
    """,
)


args = parser.parse_args()
