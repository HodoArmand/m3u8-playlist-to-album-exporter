""" .m3u8 to list[Track] parser utility class. """
import logging
import os
from pathlib import PosixPath, WindowsPath
from urllib.parse import unquote

import m3u8
from m3u8 import Segment

from exporter_stats import ExporterStats
from track import Track


class PlaylistParser:
    """ .m3u8 to list[Track] parser utility class. """

    _logger: logging.Logger = None
    _playlist_file_path: str|PosixPath|WindowsPath
    _tracks: list[Track] = []
    _stats: ExporterStats = None

    def __init__(self, playlist_file_path: str|PosixPath|WindowsPath):
        self._logger = logging.getLogger("PlaylistParser")
        self._playlist_file_path = playlist_file_path
        self._stats = ExporterStats()

    def parse_playlist(self) -> bool:
        """ Parse the .m3u8 playlist for tracks and tracknumbers. """

        self._logger.info("Loading .m3u8 playlist from file...")
        self._stats.reset()

        playlist_absolute_file_uri: str|PosixPath|WindowsPath = "file:///"+os.path.abspath(self._playlist_file_path)
        self._logger.debug("playlist_absolute_filepath: %s", playlist_absolute_file_uri)
        playlist: m3u8.M3U8

        try:
            playlist = m3u8.load(playlist_absolute_file_uri)
        except Exception as e:
            self._logger.critical("Playlist failed to load: %s",e)

            return False

        self._logger.debug("Loaded playlist content: %s", playlist.dumps())
        self._stats.total_segments = len(playlist.segments)

        for track_index, segment in enumerate(playlist.segments):
            track_uri: str = unquote(str(segment.uri))
            if not track_uri.startswith("file:///"):
                self._logger.info("Unsupported track uri. Attempting path auto repair:\n -Track: %s \n -uri: %s",
                                  segment.title,
                                  track_uri)
                repaired_uri: str|bool = self._get_repaired_uri(track_uri)
                if not repaired_uri:
                    self._logger.error("Path auto repair failed, skipping track:\n -Track: %s \n -uri: %s",segment.title, track_uri)
                    self._stats.skipped_tracks +=1

                else:
                    self._logger.info("Path auto repair successful, new track uri:\n %s", repaired_uri)
                    segment.uri = repaired_uri
                    self._stats.repaired_uris += 1

            track: Track = self._get_track_by_segment_data(track_index, segment)
            self._tracks.append(track)

        self._logger.debug("Loaded tracks: %s", self._tracks)
        self._stats.loaded_tracks = len(self._tracks)

        return True

    def get_tracks(self) -> list[Track]:
        """ Tracks getter. """

        return self._tracks

    def get_stats(self):
        """ Stats getter. """

        return self._stats

    def _get_repaired_uri(self, uri: str) -> str | bool:
        """ Repair a segment uri by prepending the directory abspath of the playlist file to it.

        Sometimes .m3u8 local playlist files don't store a full 'file:///...' abspath to the segment file,
        only the filename if it was added from the same folder.
        Example: A user dragged a new .mp3 track to the playlist from the ame folder and saved it as a .m3u8
        """

        playlist_folder_path: str|PosixPath|WindowsPath = os.path.dirname(self._playlist_file_path)
        repaired_filepath: str|PosixPath|WindowsPath = os.path.join(playlist_folder_path, uri)
        self._logger.debug("repaired_filepath: %s", repaired_filepath)
        file_abspath_from_uri: str|PosixPath|WindowsPath = os.path.abspath(repaired_filepath)

        if not os.path.isfile(file_abspath_from_uri):
            return False

        repaired_uri = "file:///"+repaired_filepath

        return repaired_uri

    @staticmethod
    def _get_track_by_segment_data(track_index: int, segment: Segment):
        """ Get a Track object from segment data. """

        track_file_abspath = os.path.abspath(unquote(str(segment.uri.replace("file:///", "", 1))))

        return Track(
            abs_file_path=track_file_abspath,
            file_name=os.path.basename(track_file_abspath),
            order=track_index + 1,
            title=segment.title,
            duration=segment.duration
        )
