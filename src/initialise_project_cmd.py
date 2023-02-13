import argparse

from structure_project_using_json import structure_project_using_json
from clean_directory import clean_directory
from save_repository import save_repository

parser = argparse.ArgumentParser(
    prog="Directory initialiser",
    description="Initialise project with JSON config file or command line arguments",
    epilog="Project directories initialised",
)
parser.add_argument(
    "--initialise",
    type=structure_project_using_json,
    help="""
    Initialises the project, using a JSON as a structure:
        \n - Directories
        \n - Files
    """,
)
parser.add_argument(
    "--clean_directory",
    type=clean_directory,
    help="""
    Will remove all files specified in the structure JSON file:
        \n - Directories
        \n - Files
    """,
)
parser.add_argument(
    "--save_directory",
    type=save_repository,
    help="""
    Will save all files specified in the structure JSON file:
        \n - Directories
        \n - Files
    """,
)


args = parser.parse_args()
