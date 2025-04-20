from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import os
import uuid

app = Flask(__name__)

DOWNLOADS_FOLDER = "downloads"
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL é obrigatória"}), 400

    try:
        video_id = str(uuid.uuid4())
        output_path = os.path.join(DOWNLOADS_FOLDER, f"{video_id}.mp4")

        ydl_opts = {
            "format": "best[ext=mp4]",
            "outtmpl": output_path,
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({"error": "Erro ao baixar o vídeo"}), 500

if __name__ == "__main__":
    app.run(debug=True)
