""" Class to hold and load the configuration values """

import logging
from argparse import Namespace
from pathlib import PosixPath, WindowsPath

import yaml

class PlaylistExporterConfiguration:
    """ Class to hold and load the configuration values """

    _logger: logging.Logger|None = None
    album_name: str|None = None
    playlist_file_path: str|None = None
    output_directory: str|None = None
    add_ordering_prefix_to_filename: bool|None = None

    def __init__(self):
        self._logger = logging.getLogger("PlaylistExporterConfiguration")

    def load_yaml(self, yaml_abspath: str|PosixPath|WindowsPath):
        """ Read the config values from a yaml file. """

        try:
            with open(yaml_abspath, 'r', encoding="utf-8") as file:
                exporter_configuration = yaml.safe_load(file)

                try:
                    self.album_name = exporter_configuration['album_name']
                    self.playlist_file_path = exporter_configuration['playlist_file_path']
                    self.output_directory = exporter_configuration['output_directory']
                    self.add_ordering_prefix_to_filename = exporter_configuration['add_ordering_prefix_to_filename']
                except KeyError as e:
                    self._logger.error("Missing key in exporter configuration: %s", e)

                # TODO: if no album name given, use the playlist filename as default.

        except Exception as e:
            self._logger.error("YAML file load error: %s", e)

    def load_argparse_namespace(self, args: Namespace):
        """ Read the config values from an argparse Namespace object when run in CLI mode. """

        try:
            self.album_name = args.album_name
            self.playlist_file_path = args.playlist_file_path
            self.output_directory = args.output_directory
            self.add_ordering_prefix_to_filename = args.add_ordering_prefix_to_filename if args.add_ordering_prefix_to_filename is not None else True
        except KeyError as e:
            self._logger.error("Missing key in exporter configuration: %s", e)

    # TODO: pull in Cerberus lib for schema validation, refactor this and the argparser part.
