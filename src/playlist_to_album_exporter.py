""" Main class of the .m3u8 playlist file to album exporter. """

import logging
from src.playlist_exporter_configuration import PlaylistExporterConfiguration


class PlaylistToAlbumExporter:
    """ Main class of the .m3u8 playlist file to album exporter. """

    _logger: logging.Logger = None
    _config: PlaylistExporterConfiguration = None

    def __init__(self, config: PlaylistExporterConfiguration):
        self._logger = logging.getLogger("PlaylistToAlbumExporter")
        self._config = config

    def export_album(self):
        """ Export the loaded tracks as a new album to the target directory. """


