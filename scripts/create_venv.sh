#!/bin/bash

cd ..
pip install virtualenv
virtualenv .venv_m3u8_playlist_to_album_exporter
source .venv_m3u8_playlist_to_album_exporter/Scripts/activate
pip install -r requirements.txt