- [Project intialiser tool](#project-intialiser-tool)
  - [How to use](#how-to-use)
  - [If you use](#if-you-use)

# Project intialiser tool

Have you ever found yourself recreating the same project directory over and over again. Well this tool solves that, the project initialiser is a `command line` application built in `python`.

## How to use

Take a look at the [example folder](https://github.com/BenjaminWills/project-initialiser/tree/master/example_usecases) to see some use cases. However I would recommend creating a `structure.json` file that has the following form:

```JSON
{
    "directories":["src","logging"],
    "files":["src/main.py","logging/log.py"]
}
```

Then to use this we simply run the command from the top level directory:

```sh
python initialise_project.py --initialise structure.json
```

If we want to clear the repository of files specified in the `structure.json` file we simply can write:

```sh
python initialise_project.py --clean_directory structure.json
```

to remove those files and directories from the project.

## If you use

If you use this, please let me know if you have any feedback!
