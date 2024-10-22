""" CLI utility runner class for the exporter. """
import os.path
from argparse import Namespace, ArgumentParser
from pathlib import WindowsPath, PosixPath

from src.playlist_to_album_exporter import PlaylistToAlbumExporter
from src.playlist_exporter_configuration import PlaylistExporterConfiguration
from src.utility.check_python_version import check_python_version

if __name__ == '__main__':

    check_python_version()
    exporter_config = PlaylistExporterConfiguration()
    parser: ArgumentParser = exporter_config.get_args_parser()
    args: Namespace = parser.parse_args()

    if args.yaml is not None:
        yaml_file_abspath: str|WindowsPath|PosixPath = os.path.abspath(args.yaml)
        exporter_config.load_yaml(yaml_file_abspath)
    else:
        exporter_config.load_argparse_namespace(args)

    exporter = PlaylistToAlbumExporter(exporter_config)
    exporter.export_album()
