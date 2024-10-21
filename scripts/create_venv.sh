#!/bin/bash

cd ..
pip install virtualenv
virtualenv .venv-m3u8-playlist-to-album-exporter
source venv/bin/activate
pip install -r requirements.txt