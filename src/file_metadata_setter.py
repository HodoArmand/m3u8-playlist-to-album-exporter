""" Class to manipulate exported track file ID3 metadata, like track order, artist and album. """

import logging
from pathlib import Path, WindowsPath, PosixPath

from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.asf import ASF
from mutagen.wave import WAVE

class FileMetadataSetter:
    """ Class to manipulate exported track file ID3 metadata, like track order, artist and album. """

    _logger: logging.Logger = None
    _track_file: EasyID3|FLAC|ASF|WAVE = None

    def __init__(self, file_abs_path: str|WindowsPath|PosixPath):
        self._logger = logging.getLogger("FileMetadataSetter")
        self._track_file = self._load_file(file_abs_path)

    def set_metadata(self, key: str, value: str):
        """ Generic method to set metadata for the audio file.
        Exceptions should be handled by the external API call's try catch.
        """

        self._logger.debug("Setting metadata '%s' to '%s'", key, value)
        self._track_file[key] = value
        self._track_file.save()
        self._logger.debug("Successfully set %s to %s", key, value)

    def set_tracknumber(self, track_number: int):
        """ Set the file's track number. """
        self.set_metadata("tracknumber", str(track_number))

    def set_album(self, album_name: str):
        """ Set the file's album. """
        self.set_metadata("album", album_name)

    def set_album_artist(self, album_artist_name: str):
        """ Set the file's album artist. """
        self.set_metadata("albumartist", album_artist_name)

    def set_artist(self, artist_name: str):
        """ Set the file's artist. """
        self.set_metadata("artist", artist_name)

    def _load_file(self, file_abs_path: Path):
        """ Load the appropriate mutagen object based on the file extension. """
        file_abs_path = Path(file_abs_path)
        extension = file_abs_path.suffix.lower()

        # Dictionary-based dispatch for handling different audio formats
        loaders = {
            '.mp3': EasyID3,  # MP3 with ID3 tags
            '.flac': FLAC,  # FLAC with Vorbis Comments
            '.wma': ASF,  # WMA with ASF metadata
            '.wav': WAVE  # WAV with limited metadata support
        }

        if extension not in loaders:
            self._logger.error("Unsupported file format: %s", extension)

            raise ValueError(f"Unsupported file format: {extension}")

        self._logger.debug("Loading %s file: %s", extension.upper(), file_abs_path)

        return loaders[extension](file_abs_path)
