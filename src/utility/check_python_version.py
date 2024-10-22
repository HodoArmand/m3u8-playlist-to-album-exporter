""" Check if the python interpreter version is up to date. """

import logging
import sys


def check_python_version():
    """ Check if the python interpreter version is up to date.
     Throws EnvironmentError, if not."""

    logger = logging.getLogger("check_python_version")

    required_minimum_version = {
        'major': 3,
        'minor': 11,
        'micro': 9,
    }
    version_info = sys.version_info

    min_version_str: str = str(required_minimum_version['major']) + str(required_minimum_version['minor']) + str(required_minimum_version['micro'])
    sys_version_str: str = str(version_info)

    if version_info.major != required_minimum_version['major']:
        error_msg = f"""Python version error: Required python major version to run this tool is:
                    {required_minimum_version['major']}. This system is running: {version_info.major}"""
        logger.error(error_msg)

        raise EnvironmentError(error_msg)

    if version_info.minor < required_minimum_version['minor'] or version_info.micro < required_minimum_version['micro']:
        error_msg = f"Python version error: Required minimum python version to run this tool is: {min_version_str}. This system is running: {sys_version_str}"
        logger.error(error_msg)

        raise EnvironmentError(error_msg)

    logger.info("Python version is up to date. Minimum required: %s System is running: %s", min_version_str, sys_version_str)
