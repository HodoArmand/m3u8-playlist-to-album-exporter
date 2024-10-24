""" Main class of the .m3u8 playlist file to album exporter. """

import logging
import os.path
import shutil
from pathlib import PosixPath, WindowsPath

from playlist_exporter_configuration import PlaylistExporterConfiguration
from exporter_stats import ExporterStats
from playlist_parser import PlaylistParser
from file_metadata_setter import FileMetadataSetter
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
            self._logger.info("Album folder created successfully.")
        except Exception as e:
            self._logger.error("Error when creating folder for album '%s' at '%s'\nerror:%s",
                               self._config.album_name,
                               self._config.output_directory,
                               e)

        # TODO: parallelize this
        # TODO: add metadata setters

        tracks: list[Track] = self._playlist_parser.get_tracks()
        tracks_len: int = len(tracks)
        for track_index, track in enumerate(tracks):
            if not os.path.isfile(track.abs_file_path):
                self._logger.error("Track %s/%s file not found. Skipping:\n -Track: %s \n -filepath: %s, ",
                                   track_index + 1,
                                    tracks_len,
                                    track.title,
                                    track.abs_file_path)
                self._stats.file_not_found_tracks += 1
            else:
                exported_track_file_abspath = self._copy_track(track_index, tracks_len, track)

                if exported_track_file_abspath:
                    self._set_track_file_metadata(track.abs_file_path, track_index + 1)

    def _copy_track(self, track_index: int, tracks_len: int, track: Track) -> str|bool:
        """ Copy the track and rename if prefixing is enambled. """

        self._logger.info("Copying track %s/%s: %s", track_index + 1, tracks_len, track.title)
        self._logger.debug("Copying track details: %s", track.title)
        try:
            output_file_abs_path: str
            if self._config.add_ordering_prefix_to_filename:
                output_file_abs_path = os.path.join(self._config.output_directory, str(track.order) + " - " + track.file_name)
            else:
                output_file_abs_path = os.path.join(self._config.output_directory, track.file_name)

            shutil.copy2(track.abs_file_path, output_file_abs_path)
            self._logger.info("Track copy done.")
            self._stats.exported_tracks += 1

        except Exception as e:
            self._logger.error("Track copy error: %s", e)

            return False

        return output_file_abs_path

    def _set_track_file_metadata(self, file_abs_path: str|PosixPath|WindowsPath, track_order: int):
        """ Set track file media metadata. """

        self._logger.info("Setting media file metadata...")
        try:
            metadata_setter = FileMetadataSetter(file_abs_path)
            metadata_setter.set_album(self._config.album_name)
            metadata_setter.set_tracknumber(track_order)
            self._logger.info("Media file metadata successfully set.")
        except Exception as e:
            self._logger.error("Media file metadata setting error: %s", e)
            self._stats.file_media_metadata_errors += 1
