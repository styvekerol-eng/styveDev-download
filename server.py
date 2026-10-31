"""
=============================================================================
          ✨ STYVEDEV DOWNLOAD PRO — Serveur Backend API (PWA)
=============================================================================
Serveur FastAPI qui expose les fonctionnalités de téléchargement via HTTP.
L'interface graphique est une Progressive Web App (PWA) servie statiquement.
Compatible PC (Windows/Mac/Linux), Android et iOS via le navigateur.
=============================================================================
"""

import os
import re
import sys
import glob
import json
import asyncio
import threading
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None

# =============================================================================
# APPLICATION FASTAPI
# =============================================================================
app = FastAPI(title="StyveDev Download Pro", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Répertoire statique (frontend PWA)
STATIC_DIR = Path(__file__).parent / "pwa"
DOWNLOADS_DIR = Path.home() / "Downloads" if sys.platform.startswith("win") else Path("/tmp/downloads")
DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# UTILITAIRES
# =============================================================================
def clean_video_url(url: str) -> str:
    url = url.strip()
    if not url:
        return url
    if ("youtube.com/watch" in url or "m.youtube.com/watch" in url) and "v=" in url:
        match = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url)
        if match:
            return f"https://www.youtube.com/watch?v={match.group(1)}"
    if "youtu.be/" in url:
        match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
        if match:
            return f"https://www.youtube.com/watch?v={match.group(1)}"
    if "&list=" in url:
        url = url.split("&list=")[0]
    return url


def format_bytes(b):
    if not b or b <= 0:
        return "Taille inconnue"
    for unit in ['o', 'Ko', 'Mo', 'Go']:
        if b < 1024.0:
            return f"{b:.1f} {unit}"
        b /= 1024.0
    return f"{b:.1f} To"


def compute_format_sizes(data):
    duration = data.get('duration') or 0
    formats = data.get('formats', [])

    audio_streams = [f for f in formats if f.get('vcodec') == 'none' and f.get('acodec') != 'none']
    best_audio_size = 0
    if audio_streams:
        audio_streams.sort(key=lambda x: (x.get('abr') or x.get('tbr') or 0), reverse=True)
        ba = audio_streams[0]
        best_audio_size = ba.get('filesize') or ba.get('filesize_approx') or 0
        if not best_audio_size and duration and (ba.get('abr') or ba.get('tbr')):
            best_audio_size = int(((ba.get('abr') or ba.get('tbr')) * 1000 / 8) * duration)

    sizes = {}
    if duration:
        sizes['mp3'] = int((320 * 1000 / 8) * duration)
    else:
        sizes['mp3'] = best_audio_size
    sizes['m4a'] = best_audio_size

    for h in [2160, 1440, 1080, 720, 480, 360]:
        matching = [
            f for f in formats
            if f.get('vcodec') != 'none' and (f.get('height') or 0) <= h and (f.get('height') or 0) > (h - 120)
        ]
        if matching:
            matching.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)
            v = matching[0]
            v_size = v.get('filesize') or v.get('filesize_approx') or 0
            if not v_size and duration and v.get('tbr'):
                v_size = int((v.get('tbr') * 1000 / 8) * duration)
            total = v_size + (best_audio_size if v.get('acodec') == 'none' else 0)
            sizes[f'{h}p'] = total

    video_streams = [f for f in formats if f.get('vcodec') != 'none']
    if video_streams:
        video_streams.sort(key=lambda x: (x.get('height') or 0, x.get('tbr') or 0), reverse=True)
        top = video_streams[0]
        ts = top.get('filesize') or top.get('filesize_approx') or 0
        if not ts and duration and top.get('tbr'):
            ts = int((top.get('tbr') * 1000 / 8) * duration)
        if top.get('acodec') == 'none':
            ts += best_audio_size
        sizes['best'] = ts
    else:
        sizes['best'] = data.get('filesize') or data.get('filesize_approx') or 0

    # Ajouter les tailles formatées
    return {k: {'bytes': v, 'human': format_bytes(v)} for k, v in sizes.items()}


# =============================================================================
# MODÈLES DE REQUÊTE
# =============================================================================
class AnalyzeRequest(BaseModel):
    url: str


class DownloadRequest(BaseModel):
    url: str
    format: str = "best"
    output_dir: Optional[str] = None


def get_local_ip() -> str:
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


# =============================================================================
# ROUTES API
# =============================================================================
@app.get("/api/health")
async def health():
    return {
        "status": "running",
        "yt_dlp": HAS_YTDLP,
        "ffmpeg": FFMPEG_PATH is not None,
        "version": "4.0.0",
        "local_ip": get_local_ip(),
        "port": 8765,
        "downloads_dir": str(DOWNLOADS_DIR)
    }


@app.get("/api/download-exe")
async def download_exe():
    exe_file = Path(__file__).parent / "StyveDev_Download_Pro.exe"
    if exe_file.exists():
        return FileResponse(
            str(exe_file),
            filename="StyveDev_Download_Pro.exe",
            media_type="application/octet-stream"
        )
    raise HTTPException(status_code=404, detail="Fichier EXE non disponible")


@app.post("/api/open-folder")
async def open_folder():
    try:
        if sys.platform == "win32":
            os.startfile(str(DOWNLOADS_DIR))
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(DOWNLOADS_DIR)])
        else:
            subprocess.Popen(["xdg-open", str(DOWNLOADS_DIR)])
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/api/analyze")
async def analyze_url(req: AnalyzeRequest):
    url = clean_video_url(req.url)
    if not url:
        raise HTTPException(status_code=400, detail="URL invalide")

    if not HAS_YTDLP:
        raise HTTPException(status_code=500, detail="yt-dlp non installé")

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _analyze_sync, url)
    return result


def _analyze_sync(url: str):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'noplaylist': True,
        'playlist_items': '1'
    }
    if FFMPEG_PATH:
        ydl_opts['ffmpeg_location'] = FFMPEG_PATH

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        data = ydl.extract_info(url, download=False)
        if 'entries' in data and data['entries']:
            data = data['entries'][0]

        sizes = compute_format_sizes(data)

        return {
            'title': data.get('title', 'Titre inconnu'),
            'uploader': data.get('uploader') or data.get('channel') or 'Auteur inconnu',
            'duration': data.get('duration', 0),
            'view_count': data.get('view_count', 0),
            'thumbnail': data.get('thumbnail'),
            'extractor': data.get('extractor_key') or data.get('extractor', 'Web'),
            'url': url,
            'sizes': sizes
        }


# =============================================================================
# WEBSOCKET POUR LE TÉLÉCHARGEMENT EN TEMPS RÉEL
# =============================================================================
@app.websocket("/ws/download")
async def download_websocket(websocket: WebSocket):
    await websocket.accept()
    cancel_flag = {"cancel": False}

    try:
        data = await websocket.receive_json()
        url = clean_video_url(data.get("url", ""))
        fmt = data.get("format", "best")
        out_dir = data.get("output_dir") or str(DOWNLOADS_DIR)

        if not url:
            await websocket.send_json({"type": "error", "message": "URL invalide"})
            return

        await websocket.send_json({"type": "status", "message": "🚀 Démarrage du téléchargement..."})

        loop = asyncio.get_event_loop()

        def progress_hook(d):
            if cancel_flag["cancel"]:
                raise Exception("CANCELLED_BY_USER")

            if d['status'] == 'downloading':
                total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
                downloaded = d.get('downloaded_bytes', 0)
                speed = d.get('speed') or 0
                eta = d.get('eta') or 0
                percent = (downloaded / total * 100) if total > 0 else 0

                msg = {
                    "type": "progress",
                    "percent": round(percent, 1),
                    "downloaded": format_bytes(downloaded),
                    "total": format_bytes(total) if total else "?",
                    "speed": f"{format_bytes(speed)}/s" if speed else "--",
                    "eta": eta
                }
                asyncio.run_coroutine_threadsafe(websocket.send_json(msg), loop)

            elif d['status'] == 'finished':
                msg = {"type": "status", "message": "🔧 Assemblage et conversion FFmpeg..."}
                asyncio.run_coroutine_threadsafe(websocket.send_json(msg), loop)

        def run_download():
            ydl_opts = {
                'outtmpl': os.path.join(out_dir, '%(title).120B [%(id)s].%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'playlist_items': '1',
                'progress_hooks': [progress_hook]
            }
            if FFMPEG_PATH:
                ydl_opts['ffmpeg_location'] = FFMPEG_PATH

            if fmt == "mp3":
                if FFMPEG_PATH:
                    ydl_opts['format'] = 'bestaudio/best'
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}]
                else:
                    ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
            elif fmt == "m4a":
                ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
            elif "1080" in fmt:
                ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif "720" in fmt:
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif "480" in fmt:
                ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]/best'
                ydl_opts['merge_output_format'] = 'mp4'
            elif "360" in fmt:
                ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]/best'
                ydl_opts['merge_output_format'] = 'mp4'
            else:
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if 'entries' in info and info['entries']:
                    info = info['entries'][0]
                filename = ydl.prepare_filename(info)
                if fmt == "mp3" and FFMPEG_PATH:
                    filename = os.path.splitext(filename)[0] + ".mp3"
                return filename

        try:
            filename = await loop.run_in_executor(None, run_download)
            file_name = os.path.basename(filename) if filename else "Fichier téléchargé"
            await websocket.send_json({
                "type": "done",
                "message": "🎉 Téléchargement terminé avec succès !",
                "filename": file_name,
                "output_dir": out_dir
            })
        except Exception as e:
            err = str(e)
            if "CANCELLED_BY_USER" in err:
                # Nettoyage des fichiers temporaires
                for p in glob.glob(os.path.join(out_dir, "*.part")):
                    try:
                        os.remove(p)
                    except Exception:
                        pass
                await websocket.send_json({"type": "cancelled", "message": "🛑 Téléchargement annulé."})
            else:
                await websocket.send_json({"type": "error", "message": err.split("\n")[0][:200]})

    except WebSocketDisconnect:
        cancel_flag["cancel"] = True
    except Exception as e:
        try:
            await websocket.send_json({"type": "error", "message": str(e)[:200]})
        except Exception:
            pass


# =============================================================================
# SERVEUR DE FICHIERS STATIQUES (FRONTEND PWA ET TÉLÉCHARGEMENTS)
# =============================================================================
# Permet de télécharger ou lire les fichiers terminés depuis un mobile ou PC
app.mount("/files", StaticFiles(directory=str(DOWNLOADS_DIR)), name="files")

if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
else:
    @app.get("/")
    async def root():
        return JSONResponse({"error": "Le dossier 'pwa/' est manquant. Lancez start.bat."})


# =============================================================================
# POINT D'ENTRÉE PRINCIPAL
# =============================================================================
def main():
    import uvicorn
    import webbrowser
    import time

    bind_host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8765))
    local_ip = get_local_ip()

    is_cloud = (
        os.environ.get("PORT") is not None
        or os.environ.get("RENDER") is not None
        or os.environ.get("SPACE_ID") is not None
        or not sys.platform.startswith("win")
    )

    # Libère automatiquement le port s'il est déjà occupé par une ancienne instance
    if not is_cloud and sys.platform == "win32":
        try:
            res = subprocess.run(f"netstat -ano | findstr :{port}", shell=True, capture_output=True, text=True)
            cur_pid = os.getpid()
            for line in res.stdout.strip().splitlines():
                if "LISTENING" in line:
                    parts = line.strip().split()
                    if len(parts) >= 5:
                        pid = int(parts[-1])
                        if pid != cur_pid and pid > 0:
                            subprocess.run(f"taskkill /f /pid {pid}", shell=True, capture_output=True)
                            time.sleep(0.5)
        except Exception:
            pass

    # Ouvre automatiquement le navigateur uniquement sur PC local
    if not is_cloud:
        def open_browser():
            time.sleep(1.2)
            webbrowser.open(f"http://127.0.0.1:{port}")

        t = threading.Thread(target=open_browser, daemon=True)
        t.start()

    print("\n" + "=" * 62)
    print("✨ STYVEDEV DOWNLOAD PRO — PWA v4.0 ACTIVE")
    print("=" * 62)
    print(f"💻 Accès Local           : http://127.0.0.1:{port}")
    print(f"📱 Accès Mobile / Réseau : http://{local_ip}:{port}")
    print(f"📁 Dossier téléchargement: {DOWNLOADS_DIR}")
    print("=" * 62)
    print("Appuyez sur CTRL+C pour arrêter le serveur.\n")

    uvicorn.run(app, host=bind_host, port=port, log_level="info")


if __name__ == "__main__":
    main()
