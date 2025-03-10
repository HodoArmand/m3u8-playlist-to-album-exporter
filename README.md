# M3U8 Playlist to Album Exporter


A simple commandline application to export music tracks from an .m3u8 playlist file to a new folder as named album, with playlist ordering of the songs.

Transform your favorite music playlists into neatly organized albums with this tool, perfect for devices like smartphones, car systems, or home audio setups.

## Example usage

After running the exporter, your music files will be organized in the specified directory with track numbers as prefixes and embedded in their metadata. If any files are missing or cannot be copied, an error message will be displayed.

### Step 1.: Create a .m3u8 playlist

Use [VLC](https://www.videolan.org/vlc/) for example to create a .m3u8 playlist file, that may contain many tracks from multiple artists, albums and folders.

<img src="https://github.com/HodoArmand/m3u8-playlist-to-album-exporter/blob/main/documentation/demo_screenshots/demo1_make_playlist_file.gif" alt="demo_image_1" loop=infinite>

### Step 2.: Configuration   

Either set up your playlist exporter configuration in a .yaml file (see _cfg_example/config_example.yaml_) or 
pass the required values as CLI arguments and flags.

_config_demo.yaml_:

`album_name: "Demo Playlist"`  
`playlist_file_path: "C:/Users/.../Desktop/demo_playlist.m3u8"`  
`output_directory: "C:/Users/.../Desktop/Demo Playlist"`  
`add_ordering_prefix_to_filename: True  `

_or as CLI args:_

`--album_name / -an "Demo Playlist"`  
`--playlist_file_path / -pf "C:/Users/.../Desktop/demo_playlist.m3u8"`  
`--output_directory / -out "C:/Users/.../Desktop/Demo Playlist"`  
`--add_ordering_prefix_to_filename / -opf`

### Step 3.: Run the exporter

Run the /scripts/run_cli.bat (Win cmd/powershell) or run_cli.sh (Bash) with:

`--yaml ".../your_config.yaml"`

or the config as CLI args.

![demo_image_2](https://github.com/HodoArmand/m3u8-playlist-to-album-exporter/blob/main/documentation/demo_screenshots/demo2_run_application.gif)

The exporter will print out the copy and metadata set stages, report any errors and provide an operation summary at the end.

Results: Your new album is ready in the designated folder with track orders and album properties set in file metadata.

![demo_image_3](https://github.com/HodoArmand/m3u8-playlist-to-album-exporter/blob/main/documentation/demo_screenshots/demo3_results.JPG)

## Installation

### Step 1.: Requirements

- Python 3.11.9 or higher
- Pip package manager

### Step 2.: Virtual python Environment

Run `scripts/create_venv.bat or .sh` to create the virtual environment.

## Configuration

An example configuration is given in the cfg_example folder.

If any of the specified paths in your configuration are invalid, the application will display an error and exit gracefully.

Full list of configuration values/CLI args and flags:

### Yaml file path `-yaml/--yaml_file_path`
Absolute path of the .yaml config file.

### Album Name `-an/--album_name` 
Name of the album.

### Playlist File Path `-pf/--playlist_file_path`  
Absolute path to the input .m3u8 playlist file.

### Output Directory `-out/--output_directory`  
Absolute path to the directory where exported files will be stored. The application will create this directory if it does not exist.

### Add Ordering Prefix To Filename `-opf/--add_ordering_prefix_to_filename`  
Enable or disable adding track ordering prefix (e.g., "1 - ", "02 -", "0358 - ") to filenames. By default, this is set to True. You can pass `True`, `False`, `yes`, `no`, `enable`, `disable`, etc. as arguments.

For example, the third file in the playlist named SongName.mp3 will have its track number set to '03' in the metadata and receive the filename "03 - SongName.mp3"

Example:
- `--add_ordering_prefix_to_filename` or `-opf` (enabled by default)
- `--add_ordering_prefix_to_filename False` or `-opf False`

### Debug Mode `-d/--debug`  
Enable debug logging for more detailed output during the execution of the application. This is useful for troubleshooting and development purposes.

By default, debug mode is disabled.

## Metadata setter supported music file formats

The following music file formats are suported for setting album and track number metadata:
- MP3
- FLAC
- WMA
- WAV

Unsupported files will still be copied and receive their track number as filename prefix if autoprefixing option is enabled.

## Troubleshooting

If you encounter an error during export, check the following:

- Verify that all file paths in your configuration are correct.
- Ensure you have read/write permissions for the specified directories.
- Check if any files are currently open or locked by other applications."

## License

Distributed under GNU GPL v3 license. See [LICENSE](https://github.com/HodoArmand/m3u8-playlist-to-album-exporter/blob/main/LICENSE) for more information. 
