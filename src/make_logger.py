import logging
import os


def add_file_output(logger: logging.Logger, logging_path: str, formatter_style: str):
    file_handler = logging.FileHandler(logging_path)
    formatter = logging.Formatter(formatter_style)

    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)


def make_logger(
    logging_path: str = os.getcwd() + "/" + __name__ + ".log",
    save_logs: bool = True,
    formatter_style: str = "%(asctime)s - %(name)s - %(levelname)s :: %(message)s",
    logger_name: str = __name__,
    logger_level: int = logging.INFO,
) -> logging.Logger:

    # Create logger
    logger = logging.getLogger(name=logger_name)
    # Set urgency level
    logger.setLevel(logger_level)

    if save_logs:
        add_file_output(logger, logging_path, formatter_style)

    return logger
