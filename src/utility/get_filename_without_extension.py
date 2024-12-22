""" Get filename without extension from a file path. """

from pathlib import Path, PosixPath, WindowsPath


def get_filename_without_extension(file_path: str|PosixPath|WindowsPath):
    """ Get filename without extension from a file path. """

    return Path(file_path).stem
