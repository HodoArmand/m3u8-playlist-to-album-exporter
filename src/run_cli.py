""" CLI utility runner class for the exporter. """

import argparse
from argparse import Namespace


class RunCli:
    """ Run the application as a CLI tool. """

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog=".m3u8 Album Exporter CLI utility", description = '')
    parser.add_argument('-yaml', '--yaml_file_path', help='TODO: fill this')
    parser.add_argument('-an', '--album_name', help='TODO: fill this')
    parser.add_argument('-pf', '--playlist_file_path', help='TODO: fill this')
    parser.add_argument('-out', '--output_directory', help='TODO: fill this')
    parser.add_argument('-opf', '--add_ordering_prefix_to_filename', help='TODO: fill this')
    args: Namespace = parser.parse_args()
