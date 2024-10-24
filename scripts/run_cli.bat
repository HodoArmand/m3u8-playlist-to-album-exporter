@echo off
cd ..
echo "Activating the virtual environment"
call .venv_m3u8_playlist_to_album_exporter\Scripts\activate

echo "Running the Album Exporter..."
python src\run_cli.py %*