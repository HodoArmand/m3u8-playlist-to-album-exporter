@echo off
cd ..
echo "Installing virtualenv if not already installed..."
pip install virtualenv

echo "Creating the virtual environment..."
virtualenv .venv_m3u8_playlist_to_album_exporter

echo "Activating the virtual environment..."
call .venv_m3u8_playlist_to_album_exporter\Scripts\activate

echo "Installing the required packages..."
pip install -r requirements.txt