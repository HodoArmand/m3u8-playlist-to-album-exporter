""" Soundtrack descriptor tuple. """

from pathlib import PosixPath, WindowsPath
from typing import NamedTuple


class Track(NamedTuple):
    """ Soundtrack descriptor tuple. """
    abs_file_path: str|PosixPath|WindowsPath
    file_name: str
    order: int
    title: str
    duration: int

    def __str__(self):
        return "[\nabs_file_path:"+str(self.abs_file_path)+\
            "\nfile_name:"+self.file_name+\
            "\norder:"+str(self.order)+\
            "\ntitle:"+self.title+\
            "\nduration:"+str(self.duration)+"\n]"
