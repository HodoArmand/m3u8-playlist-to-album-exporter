#!/bin/bash

cd ..

source .venv_m3u8_playlist_to_album_exporter/Scripts/activate

python src/run_cli.py "$@"