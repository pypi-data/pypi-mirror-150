import os
import json
import logging

from io import TextIOWrapper
from hashlib import md5
from logging.handlers import RotatingFileHandler
from typing import Any, List, Union


def create_path(path: str) -> None:
    """
    Creates path recursively

    :param path: str Path to be created

    :return: None
    """

    # If target is file ..
    if os.path.splitext(path)[1].lower() in ['.html', '.json']:
        # .. use its directory as target
        path = os.path.dirname(path)

    # Create it
    if not os.path.exists(path):
        try:
            os.makedirs(path)

        # Guard against race condition
        except OSError:
            pass


def flatten(data: List[list]) -> List[Any]:
    """
    Flattens list of lists (async version)

    :param data: list List of lists

    :return: list Flattened list
    """

    return [item for sublist in data for item in sublist]


def get_logger(log_dir: str, log_name: str) -> logging.Logger:
    """
    Initializes logger & implements logfile rotation

    :param log_dir: str Logs directory
    :param log_name: str Log filename

    :return: logging.Logger
    """

    # Initialize logger
    logger = logging.getLogger(__name__)

    # Set loglevel
    logger.setLevel(logging.INFO)

    # Configure log handler
    log_handler = RotatingFileHandler(
        filename = os.path.join(log_dir, log_name),
        maxBytes = 1024 * 1024,
        backupCount = 5
    )

    # Implement formatting
    log_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s: %(levelname)-8s %(message)s'))

    # Add log handler to logger
    logger.addHandler(log_handler)

    return logger


def data2hash(data: Any) -> str:
    """
    Builds hash over given data

    :param data: typing.Any Data

    :return: str Hash
    """

    return md5(str(data).encode('utf-8')).hexdigest()


def list2chunks(data: list, size: int) -> List[list]:
    """
    Splits list into chunks

    :param data: list Data to be split
    :param size: int Chunk size

    :return: list<list> Chunks
    """

    # Split data into smaller chunks
    return [data[i:i + size] for i in range(0, len(data), size)]


# FILE I/O

def load_json(json_file: Union[str, TextIOWrapper]) -> Union[list, dict]:
    """
    Loads data from JSON

    :param json_file: str|io.TextIOWrapper Path to JSON file OR text stream

    :return: dict|list Data
    :raises: Exception Decoding error
    """

    try:
        if isinstance(json_file, str):
            with open(json_file, 'r') as file:
                return json.load(file)

        return json.load(json_file)

    except json.decoder.JSONDecodeError:
        raise Exception

    return {}


def dump_json(data: Union[dict, list], json_file: Union[str, TextIOWrapper]) -> None:
    """
    Dumps JSON data to file

    :param data: dict|list Data
    :param json_file: str|io.TextIOWrapper Path to JSON file OR text stream

    :return: None
    """

    if isinstance(json_file, str):
        # Create path (if needed)
        create_path(json_file)

        # Store data
        with open(json_file, 'w') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    else:
        json.dump(data, json_file, ensure_ascii=False, indent=4)
