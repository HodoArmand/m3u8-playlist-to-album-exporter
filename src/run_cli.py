""" CLI utility runner class for the exporter. """
import logging
import os.path
from argparse import Namespace, ArgumentParser
from pathlib import WindowsPath, PosixPath

from playlist_to_album_exporter import PlaylistToAlbumExporter
from playlist_exporter_configuration import PlaylistExporterConfiguration
from utility.check_python_version import check_python_version

def run_cli() -> int:
    """ Run the CLI API for the application """

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger("Playlist Exporter CLI Utility")

    check_python_version()
    exporter_config = PlaylistExporterConfiguration()
    parser: ArgumentParser = exporter_config.get_args_parser()
    args: Namespace = parser.parse_args()

    try:
        yaml_file_abspath: str | WindowsPath | PosixPath = os.path.abspath(args.yaml_file_path)
        exporter_config.load_yaml(yaml_file_abspath)
    except TypeError:
        logger.info("No yaml file path argument given, loading configuration from CLI args...")
        exporter_config.load_argparse_namespace(args)

    if not exporter_config.is_loaded():
        logger.error("Configuration failed to load.")

        return 1

    exporter = PlaylistToAlbumExporter(exporter_config)
    exporter.export_album()

    return 0


if __name__ == '__main__':
    run_cli()
