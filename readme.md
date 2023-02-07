- [Project intialiser tool](#project-intialiser-tool)
  - [How to use](#how-to-use)

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
python
```
