""" CLI utility runner class for the exporter. """
import os.path
import argparse
from argparse import Namespace
from pathlib import WindowsPath, PosixPath

from src.playlist_to_album_exporter import PlaylistToAlbumExporter
from src.playlist_exporter_configuration import PlaylistExporterConfiguration
from src.utility.check_python_version import check_python_version

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=".m3u8 Album Exporter CLI utility", description = '')
    parser.add_argument('-yaml', '--yaml_file_path', help='TODO: fill this')
    parser.add_argument('-an', '--album_name', help='TODO: fill this')
    parser.add_argument('-pf', '--playlist_file_path', help='TODO: fill this')
    parser.add_argument('-out', '--output_directory', help='TODO: fill this')
    parser.add_argument('-opf', '--add_ordering_prefix_to_filename', help='TODO: fill this')
    args: Namespace = parser.parse_args()

    check_python_version()

    exporter_config = PlaylistExporterConfiguration()
    if args.yaml is not None:
        yaml_file_abspath: str|WindowsPath|PosixPath = os.path.abspath(args.yaml)
        exporter_config.load_yaml(yaml_file_abspath)
    else:
        exporter_config.load_argparse_namespace(args)

    exporter = PlaylistToAlbumExporter(exporter_config)
    exporter.export_album()