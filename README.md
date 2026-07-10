# yt-downloader-web

Simple local web app for downloading YouTube videos, with a quality picker. Flask + [yt-dlp](https://github.com/yt-dlp/yt-dlp) + ffmpeg.

## Requirements

- Python 3
- ffmpeg (`sudo apt install ffmpeg`)

## Setup

```bash
python3 -m venv .venv
./.venv/bin/pip install -r requirements.txt
```

## Usage

```bash
./.venv/bin/python app.py
```

Open `http://127.0.0.1:5000` in your browser, paste a YouTube URL, pick a quality (`360p`–`1080p`, `best`, or `audio`), and click Download. The file streams straight to your browser's downloads folder — nothing is kept on the server afterward.
