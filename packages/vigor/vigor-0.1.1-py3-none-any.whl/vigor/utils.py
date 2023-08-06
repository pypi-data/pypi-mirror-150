import os
import sys
import logging
import subprocess

from abc import ABC
from typing import List


class CommandRunner(ABC):
    def __init__(self, logging_level: int=logging.INFO):
        """
        Constructor for CommandRunner.

        CommandRunner is an ABC that implements the basic function of run, which runs
        some given CLI command. More specific use-cases should inherit from CommandRunner,
        instead of implementing specific one-off calls to CommandRunner.run().

        Args:
            logging_level (int, optional): Logging level. Defaults to logging.INFO.
        """
        configure_logger()

    def run(self, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Run some CLI command, constructed from args and kwargs.

        Returns:
            subprocess.CompletedProcess: Completed Process, which will contain output
            and exit codes.
        """
        logging.info(f"Command: {args}")
        sys.stdout.flush()

        try:
            return subprocess.run(args, shell=False, check=True, cwd=os.path.join(os.path.dirname(__file__), ".."), encoding='utf-8', **kwargs)
        except subprocess.CalledProcessError as e:
            error_message = f"""
                The command exited with an error:
                {args}
                {e.stdout if e.stdout else ""}
                {e.stderr if e.stderr else ""}
            """

            logging.error(error_message)
            raise


def configure_logger(logging_level: int=logging.INFO):
    """
    Configures logger.

    Args:
        logging_level (int, optional): Logging level. Defaults to logging.INFO.
    """
    logger = logging.getLogger()
    logger.setLevel(level=logging_level)


def get_immediate_subdirectories(full_path: str, ignore: List=[], absolute_path=True) -> List:
    """
    Get all immediate sub-directories for a certain full path.

    Args:
        full_path (str): Full path to folder to get immediate sub-directories for.
        ignore (List): List of folders to ignore. Defaults to [].

    Returns:
        List: List of immediate sub-directories.
    """
    subdirectories = []
    for item in os.scandir(full_path):
        if item.is_dir() and item.name not in ignore:
            if absolute_path:
                subdirectories.append(item.path)
            else:
                subdirectories.append(item.name)

    return subdirectories
