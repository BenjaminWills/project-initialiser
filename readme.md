- [Project intialiser tool](#project-intialiser-tool)
  - [How to use](#how-to-use)
    - [`initialise_project.py`](#initialise_projectpy)
    - [`make_logger.py`](#make_loggerpy)
    - [SQL wrapper](#sql-wrapper)
  - [If you use](#if-you-use)

# Project intialiser tool

Have you ever found yourself recreating the same project directory over and over again. Well this tool solves that, the project initialiser is a `command line` application built in `python`.

## How to use

### [`initialise_project.py`](https://github.com/BenjaminWills/project-initialiser/blob/master/src/initialise_project.py)

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

### [`make_logger.py`](https://github.com/BenjaminWills/project-initialiser/blob/master/src/make_logger.py)

This is a script that can be used to make a custom logger easily.

```python
# file.py
from logging import INFO
import make_logger.py

my_logger = make_logger(
  logging_path = "my_path/my_logs.log",
  save_logs = True,
  formatter_style = "%(asctime)s - %(name)s - %(levelname)s :: %(message)s",
  logger_name = "my_logger",
  logger_level = INFO
)

if __name__ == "__main__":
    my_logger.info("My first log!")
    my_logger.warning("AAAAH")
```

Now the `log` file looks like:

```log
2023-02-08 19:50:06,078 - my_logger - INFO :: My first log!
2023-02-08 19:50:06,078 - my_logger - WARNING :: AAAAH
```

### SQL wrapper

This is a class to use to connect to an SQL database, it can be modified to fit other databases that aren't `PostgreSQL`. An example `postgres` database is @ [rfam PostgreSQL database](https://docs.rfam.org/en/latest/database.html)

```python
import Sql_Wrapper

db_username="rfamro"
db_password=""
db_host="mysql-rfam-public.ebi.ac.uk"
db_port=4497
db_name="Rfam"

sql = Sql_Wrapper(
  db_username,
  db_password,
  db_host,
  db_port,
  db_name
)

print(
  sql.
)
```

## If you use

If you use this, please let me know if you have any feedback!
