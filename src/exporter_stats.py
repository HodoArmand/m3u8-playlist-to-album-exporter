""" Dataclass to hold exporter statistics. """


# Reason: Eight is reasonable in this case.
# pylint: disable-next=too-many-instance-attributes
class ExporterStats:
    """ Dataclass to hold exporter statistics. """
    total_segments: int = 0
    repaired_uris: int = 0
    skipped_tracks: int = 0
    loaded_tracks: int = 0
    file_not_found_tracks: int = 0
    copy_error_tracks: int = 0
    file_media_metadata_errors: int = 0
    exported_tracks: int = 0

    def reset(self):
        """ Set all stats to zero. """

        self.total_segments = 0
        self.repaired_uris = 0
        self.skipped_tracks = 0
        self.loaded_tracks = 0
        self.file_not_found_tracks = 0
        self.copy_error_tracks = 0
        self.file_media_metadata_errors = 0
        self.exported_tracks = 0

    def __str__(self):
        return "[\ntotal_segments:"+str(self.total_segments)+\
            "\npath_autorepaired_tracks:"+str(self.repaired_uris)+\
            "\nskipped_tracks:"+str(self.skipped_tracks)+\
            "\nloaded_tracks:"+str(self.loaded_tracks)+\
            "\nfile_not_found_tracks:"+str(self.file_not_found_tracks)+\
            "\ncopy_error_tracks:"+str(self.copy_error_tracks)+\
            "\nfile_media_metadata_errors:"+str(self.copy_error_tracks)+\
            "\nexported_tracks:"+str(self.exported_tracks)+"\n]"

    def __add__(self, other):

        summed_stats = ExporterStats()
        summed_stats.total_segments = self.total_segments + other.total_segments
        summed_stats.repaired_uris = self.repaired_uris + other.repaired_uris
        summed_stats.skipped_tracks = self.skipped_tracks + other.skipped_tracks
        summed_stats.loaded_tracks = self.loaded_tracks + other.loaded_tracks
        summed_stats.file_not_found_tracks = self.file_not_found_tracks + other.file_not_found_tracks
        summed_stats.copy_error_tracks = self.copy_error_tracks + other.copy_error_tracks
        summed_stats.file_media_metadata_errors = self.file_media_metadata_errors + other.file_media_metadata_errors
        summed_stats.exported_tracks = self.exported_tracks + other.exported_tracks

        return summed_stats
