""" Main class of the .m3u8 playlist file to album exporter. """

import logging
import os.path
import shutil
from pathlib import PosixPath, WindowsPath
from typing import NamedTuple
from urllib.parse import unquote

import m3u8

from playlist_exporter_configuration import PlaylistExporterConfiguration

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

class PlaylistToAlbumExporter:
    """ Main class of the .m3u8 playlist file to album exporter. """

    _logger: logging.Logger = None
    _config: PlaylistExporterConfiguration = None
    _tracks: list[Track] = []

    def __init__(self, config: PlaylistExporterConfiguration):
        self._logger = logging.getLogger("PlaylistToAlbumExporter")
        self._config = config

    def __str__(self):
        raise NotImplementedError
        # TODO: this

    def print_preview(self):
        """ Print the preview of the export operation with the current configuration. """
        raise NotImplementedError
        # TODO: this

    def export_album(self) -> bool:
        """ Export the loaded tracks as a new album to the target directory. """
        if not self._parse_playlist():
            self._logger.error("Playlist failed to load, export disabled, exiting. ")

            return False

        self._logger.info("Exporting Album...")

        self._copy_and_set_metadata()

        return True

    def _parse_playlist(self) -> bool:
        """ Parse the .m3u8 playlist for tracks and tracknumbers. """

        self._logger.info("Loading .m3u8 playlist from file...")

        playlist_absolute_filepath: str|PosixPath|WindowsPath = "file:///"+os.path.abspath(self._config.playlist_file_path)
        self._logger.debug("playlist_absolute_filepath: %s", playlist_absolute_filepath)
        playlist: m3u8.M3U8

        try:
            playlist = m3u8.load(playlist_absolute_filepath)
        except Exception as e:
            self._logger.error("Playlist failed to load: %s",e)

            return False

        self._logger.debug("Loaded playlist content: %s", playlist.dumps())

        for track_index, segment in enumerate(playlist.segments):
            track_uri: str = str(segment.uri)
            if not track_uri.startswith("file:///"):
                self._logger.info("Unsupported track uri. Skipping:\n -Track: %s \n -uri: %s, ",
                                  segment.title,
                                  track_uri)
            else:
                abs_file_path = unquote(track_uri.replace("file:///", "", 1))
                self._tracks.append(
                    Track(
                        abs_file_path=abs_file_path,
                        file_name=os.path.basename(abs_file_path),
                        order=track_index+1,
                        title=segment.title,
                        duration=segment.duration
                    )
                )

        self._logger.debug("Loaded tracks: %s", self._tracks)

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
        # TODO: add stats, print it (total loaded, ok, skipped, errored, etc.)
        for track in self._tracks:
            if not os.path.isfile(track.abs_file_path):
                self._logger.error("Track file not found. Skipping:\n -Track: %s \n -uri: %s, ",
                                  track.title,
                                  track.abs_file_path)
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

                except Exception as e:
                    self._logger.error("Error when copying track '%s', error:%s", track.title, e)
