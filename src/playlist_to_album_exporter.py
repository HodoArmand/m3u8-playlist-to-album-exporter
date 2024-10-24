""" Main class of the .m3u8 playlist file to album exporter. """

import logging
import os.path
import shutil

from playlist_exporter_configuration import PlaylistExporterConfiguration
from exporter_stats import ExporterStats
from playlist_parser import PlaylistParser
from track import Track


class PlaylistToAlbumExporter:
    """ Main class of the .m3u8 playlist file to album exporter. """

    _logger: logging.Logger = None
    _config: PlaylistExporterConfiguration = None
    _stats: ExporterStats = None
    _playlist_parser: PlaylistParser = None
    _export_enabled: bool = False
    _tracks: list[Track] = []

    def __init__(self, config: PlaylistExporterConfiguration):
        self._logger = logging.getLogger("PlaylistToAlbumExporter")
        self._config = config
        self._stats = ExporterStats()
        self._playlist_parser = PlaylistParser(self._config.playlist_file_path)

    def parse_playlist(self) -> bool:
        """ Parse the playlist, enable export if successful. """

        self._logger.info("Parsing playlist...")
        if not self._playlist_parser.parse_playlist():
            self._logger.error("Playlist failed to load, export disabled, exiting. ")

            return False

        self._logger.info("Parsing successful.")
        self._stats += self._playlist_parser.get_stats()
        self._export_enabled = True

        return True

    def export_album(self) -> bool:
        """ Export the loaded tracks as a new album to the target directory. """

        if not self._export_enabled:
            self._logger.error("Album export is disabled. Successfully parse a playlist first.")

            return False

        self._logger.info("Exporting Album...")
        self._copy_and_set_metadata()
        self._logger.info("Export finished, statistics: %s", self._stats)

        return True

    def _copy_and_set_metadata(self):
        """ Copy the loaded tracks into the designated album folder.
         Set album and track # metadata.
         Rename file with track number prefix is configured true. """

        self._logger.info("Creating folder for album %s", self._config.album_name)
        try:
            os.makedirs(self._config.output_directory, exist_ok=True)
        except Exception as e:
            self._logger.error("Error when creating folder for album '%s' at '%s'\nerror:%s",
                               self._config.album_name,
                               self._config.output_directory,
                               e)

        # TODO: parallelize this
        # TODO: add metadata setters
        for track in self._playlist_parser.get_tracks():
            if not os.path.isfile(track.abs_file_path):
                self._logger.error("Track file not found. Skipping:\n -Track: %s \n -uri: %s, ",
                                  track.title,
                                  track.abs_file_path)
                self._stats.file_not_found_tracks += 1
            else:
                self._logger.info("Copying track: %s", track.title)
                self._logger.debug("Copying track details: %s", track.title)
                try:
                    output_file_abs_path: str
                    if self._config.add_ordering_prefix_to_filename:
                        output_file_abs_path = os.path.join(self._config.output_directory, str(track.order)+" - "+track.file_name)
                    else:
                        output_file_abs_path = os.path.join(self._config.output_directory, track.file_name)

                    shutil.copy2(track.abs_file_path, output_file_abs_path)
                    self._logger.info("Track copy done: %s", track.title)
                    self._stats.exported_tracks +=1

                except Exception as e:
                    self._logger.error("Error when copying track '%s', error:%s", track.title, e)
