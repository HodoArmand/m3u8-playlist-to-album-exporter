""" Class to hold and load the configuration values """
import argparse
import logging
import os.path
from argparse import Namespace, ArgumentParser
from pathlib import PosixPath, WindowsPath
from typing import NamedTuple

import yaml

from src.utility.get_filename_without_extension import get_filename_without_extension


class PlaylistExporterConfigurationValues(NamedTuple):
    """ Named tuple to hold exporter configuration values. """
    album_name: str|None = None
    playlist_file_path: str|None = None
    output_directory: str|None = None
    add_ordering_prefix_to_filename: bool|None = None

class PlaylistExporterConfiguration:
    """ Class to hold and load the configuration values from code, yaml or cli args. """

    _logger: logging.Logger|None = None
    album_name: str|None = None
    playlist_file_path: str|None = None
    output_directory: str|None = None
    add_ordering_prefix_to_filename: bool|None = True

    def __init__(self):
        self._logger = logging.getLogger("PlaylistExporterConfiguration")

    def load_tuple(self, values: PlaylistExporterConfigurationValues):
        """ Class prop initialization from named tuple. """

        self._logger = logging.getLogger("PlaylistExporterConfiguration")
        self.album_name = values.album_name
        self.playlist_file_path = values.playlist_file_path
        self.output_directory = values.output_directory
        self.add_ordering_prefix_to_filename = values.add_ordering_prefix_to_filename

    def load_yaml(self, yaml_abspath: str|PosixPath|WindowsPath):
        """ Read the config values from a yaml file. """

        try:
            with open(yaml_abspath, 'r', encoding="utf-8") as file:
                config = yaml.safe_load(file)

                try:
                    if config["playlist_file_path"] is not None and config["album_name"] is None:
                        config["album_name"] = get_filename_without_extension(config["playlist_file_path"])
                    if config["output_directory"] is not None and config["album_name"] is None:
                        config["output_directory"] = os.path.join("output", os.path.abspath(get_filename_without_extension(config["playlist_file_path"])))
                    if config["output_directory"] is not None and config["album_name"] is not None:
                        config["output_directory"] = os.path.join("output", os.path.abspath(config["album_name"]))

                    config["add_ordering_prefix_to_filename"] = config["add_ordering_prefix_to_filename"] if config["add_ordering_prefix_to_filename"] is not None else True

                    config_tuple = PlaylistExporterConfigurationValues(
                        album_name=config["album_name"],
                        playlist_file_path=config["playlist_file_path"],
                        output_directory=config["output_directory"],
                        add_ordering_prefix_to_filename=config["add_ordering_prefix_to_filename"]
                    )

                    self.load_tuple(config_tuple)

                except KeyError as e:
                    self._logger.error("Missing key in exporter configuration: %s", e)

        except Exception as e:
            self._logger.error("YAML file load error: %s", e)

    @staticmethod
    def get_args_parser() -> ArgumentParser:
        """ Get an argparse object for the CLI config input. """

        parser = argparse.ArgumentParser(prog=".m3u8 Album Exporter CLI utility", description='TODO: fill this')
        parser.add_argument('-yaml', '--yaml_file_path', help='TODO: fill this')
        parser.add_argument('-an', '--album_name', help='TODO: fill this')
        parser.add_argument('-pf', '--playlist_file_path', help='TODO: fill this')
        parser.add_argument('-out', '--output_directory', help='TODO: fill this')
        parser.add_argument('-opf', '--add_ordering_prefix_to_filename', help='TODO: fill this')

        return parser

    def load_argparse_namespace(self, config: Namespace):
        """ Read the config values from an argparse Namespace object when run in CLI mode. """

        try:
            if config.playlist_file_path is not None and config.album_name is None:
                config.album_name = get_filename_without_extension(config.playlist_file_path)
            if config.output_directory is not None and config.album_name is None:
                config.output_directory = os.path.join("output", os.path.abspath(get_filename_without_extension(config.playlist_file_path)))
            if config.output_directory is not None and config.album_name is not None:
                config.output_directory = os.path.join("output", os.path.abspath(config.album_name))

            config.add_ordering_prefix_to_filename = config.add_ordering_prefix_to_filename if config.add_ordering_prefix_to_filename is not None else True

            config_tuple = PlaylistExporterConfigurationValues(
                album_name=config.album_name,
                playlist_file_path=config.playlist_file_path,
                output_directory=config.output_directory,
                add_ordering_prefix_to_filename=config.add_ordering_prefix_to_filename
            )

            self.load_tuple(config_tuple)

        except KeyError as e:
            self._logger.error("Missing key in exporter configuration: %s", e)

    # TODO: pull in Cerberus lib for schema validation, refactor this and the argparser part.
