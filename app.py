import os
import tempfile
import shutil

from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from yt_dlp import YoutubeDL

app = Flask(__name__)
app.secret_key = "local-dev-only"

QUALITY_CHOICES = ["360p", "480p", "720p", "1080p", "best", "audio"]


def build_format(quality: str) -> str:
    if quality == "best":
        return "bestvideo+bestaudio/best"
    if quality == "audio":
        return "bestaudio/best"
    height = quality.rstrip("p")
    return f"bestvideo[height<={height}]+bestaudio/best[height<={height}]"


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", qualities=QUALITY_CHOICES)


@app.route("/download", methods=["POST"])
def download():
    url = request.form.get("url", "").strip()
    quality = request.form.get("quality", "720p")

    if not url:
        flash("Please paste a YouTube URL.")
        return redirect(url_for("index"))

    tmp_dir = tempfile.mkdtemp(prefix="ytdl_")
    ydl_opts = {
        "format": build_format(quality),
        "outtmpl": f"{tmp_dir}/%(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith(".mp4") and quality != "audio":
                filename = os.path.splitext(filename)[0] + ".mp4"

        response = send_file(filename, as_attachment=True)

        @response.call_on_close
        def cleanup():
            shutil.rmtree(tmp_dir, ignore_errors=True)

        return response
    except Exception as exc:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        flash(f"Download failed: {exc}")
        return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
