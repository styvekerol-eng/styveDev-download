"""
=============================================================================
                     ✨ STYVEDEV DOWNLOAD PRO ✨
=============================================================================
Application moderne, luxueuse et multi-plateformes de téléchargement vidéo & audio.
Compatible avec :
  - 🔴 YouTube (4K, 1080p, 720p, Short, MP3)
  - 🔵 Facebook (Vidéos, Reels, Watch)
  - 🟣 Instagram (Reels, Vidéos, Stories)
  - 🎵 TikTok (Vidéos HD, Sans filigrane lorsque disponible)
  - ✖️ Twitter / X
  - 👾 Twitch (Clips, VODs)
  - 🤖 Reddit
  - 🌐 + de 1500 sites supportés

Fonctionnalités avancées :
  - CALCUL & AFFICHAGE DE LA TAILLE EXACTE AVANT TÉLÉCHARGEMENT
  - Support complet et dynamique des thèmes SOMBRE, CLAIR et SYSTÈME
  - Mode vidéo unique strict (bloque le téléchargement en boucle des Mix/Playlists)
  - Bouton d'arrêt d'urgence instantané (🛑 Arrêter le téléchargement)
  - Nettoyage automatique des fichiers temporaires (.part)
  - Historique de session avec lecture directe
=============================================================================
"""

import os
import sys
import re
import glob
import time
import threading
import urllib.request
from io import BytesIO
from tkinter import filedialog, messagebox

import customtkinter as ctk
from PIL import Image

# Moteur principal : yt-dlp
try:
    import yt_dlp
    HAS_YTDLP = True
except ImportError:
    HAS_YTDLP = False

# Moteur FFmpeg pour la conversion et l'assemblage audio/vidéo
try:
    import imageio_ffmpeg
    FFMPEG_PATH = imageio_ffmpeg.get_ffmpeg_exe()
except Exception:
    FFMPEG_PATH = None

# Fallback secondaire
try:
    from pytubefix import YouTube
    HAS_PYTUBEFIX = True
except ImportError:
    try:
        from pytube import YouTube
        HAS_PYTUBEFIX = True
    except ImportError:
        HAS_PYTUBEFIX = False


# =============================================================================
# DESIGN SYSTEM DUAL (CLAIR / SOMBRE DYNAMIQUE)
# =============================================================================
THEME = {
    "bg_main": ("#F1F5F9", "#0B0F19"),
    "card_bg": ("#FFFFFF", "#131C2E"),
    "card_border": ("#E2E8F0", "#1E293B"),
    "input_bg": ("#F8FAFC", "#0D1525"),
    "input_border": ("#CBD5E1", "#334155"),
    "text_main": ("#0F172A", "#F8FAFC"),
    "text_muted": ("#64748B", "#94A3B8"),
    "text_title": ("#1E40AF", "#60A5FA"),
    "badge_bg": ("#F1F5F9", "#0F172A"),
    "badge_text": ("#0369A1", "#38BDF8"),
    "badge_version_bg": ("#DBEAFE", "#1E3A8A"),
    "badge_version_text": ("#1D4ED8", "#93C5FD"),
    "badge_size_bg": ("#DCFCE7", "#064E3B"),
    "badge_size_text": ("#15803D", "#34D399"),
    "btn_sec_bg": ("#E2E8F0", "#1E293B"),
    "btn_sec_hover": ("#CBD5E1", "#334155"),
    "btn_sec_text": ("#1E293B", "#F8FAFC"),
    "accent_blue": ("#2563EB", "#2563EB"),
    "accent_hover": ("#1D4ED8", "#1D4ED8"),
    "accent_danger": ("#DC2626", "#DC2626"),
    "accent_danger_hover": ("#B91C1C", "#B91C1C"),
    "progress_track": ("#E2E8F0", "#0F172A"),
    "status_color": ("#2563EB", "#60A5FA"),
    "checkbox_text": ("#0284C7", "#38BDF8"),
    "hist_item_bg": ("#F8FAFC", "#0F172A"),
    "hist_item_text": ("#0F172A", "#F1F5F9")
}

PLATFORMS = [
    ("🔴 YouTube", "#EF4444"),
    ("🔵 Facebook", "#1877F2"),
    ("🟣 Instagram", "#E1306C"),
    ("🎵 TikTok", ("#008080", "#00F2FE")),
    ("✖️ Twitter / X", ("#475569", "#A1A1AA")),
    ("👾 Twitch", "#9146FF"),
    ("🤖 Reddit", "#FF4500"),
    ("🌐 1500+ Sites", "#3B82F6")
]


# =============================================================================
# UTILITAIRES & CALCUL DE TAILLE
# =============================================================================
def clean_video_url(url: str, force_single: bool = True) -> str:
    url = url.strip()
    if not url:
        return url

    if force_single:
        if ("youtube.com/watch" in url or "m.youtube.com/watch" in url) and "v=" in url:
            match = re.search(r"[?&]v=([a-zA-Z0-9_-]{11})", url)
            if match:
                return f"https://www.youtube.com/watch?v={match.group(1)}"

        if "youtu.be/" in url:
            match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
            if match:
                return f"https://www.youtube.com/watch?v={match.group(1)}"

        if "&list=" in url and ("watch" in url or "fb.watch" in url or "tiktok.com" in url or "instagram.com" in url):
            url = url.split("&list=")[0]

    return url


def detect_platform(url: str):
    u = url.lower()
    if "youtube.com" in u or "youtu.be" in u:
        return "YouTube", "🔴 YouTube", "#EF4444"
    if "facebook.com" in u or "fb.watch" in u or "fb.com" in u:
        return "Facebook", "🔵 Facebook", "#1877F2"
    if "instagram.com" in u:
        return "Instagram", "🟣 Instagram", "#E1306C"
    if "tiktok.com" in u:
        return "TikTok", "🎵 TikTok", ("#008080", "#00F2FE")
    if "twitter.com" in u or "x.com" in u:
        return "Twitter / X", "✖️ Twitter / X", ("#475569", "#A1A1AA")
    if "twitch.tv" in u:
        return "Twitch", "👾 Twitch", "#9146FF"
    if "reddit.com" in u:
        return "Reddit", "🤖 Reddit", "#FF4500"
    if "vimeo.com" in u:
        return "Vimeo", "🎬 Vimeo", "#1AB7EA"
    if "dailymotion.com" in u:
        return "Dailymotion", "📺 Dailymotion", "#0066DC"
    if u.strip():
        return "Web Universel", "🌐 Web Universel", "#3B82F6"
    return "Aucun", "🌐 Prêt", ("#64748B", "#94A3B8")


def format_bytes(bytes_count):
    if not bytes_count or bytes_count <= 0:
        return "Taille inconnue"
    for unit in ['o', 'Ko', 'Mo', 'Go']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.1f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.1f} To"


def format_duration(seconds):
    if not seconds:
        return "00:00"
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"


def format_views(count):
    if not count:
        return ""
    count = int(count)
    if count >= 1_000_000:
        return f"{count / 1_000_000:.1f}M vues"
    if count >= 1_000:
        return f"{count / 1_000:.1f}k vues"
    return f"{count} vues"


def compute_all_format_sizes(data):
    """
    Calcule précisément la taille de chaque format (en octets)
    à partir des métadonnées des flux vidéo et audio avant téléchargement.
    """
    duration = data.get('duration') or 0
    formats = data.get('formats', [])

    # Trouver le meilleur flux audio
    audio_streams = [
        f for f in formats 
        if f.get('vcodec') == 'none' and f.get('acodec') != 'none'
    ]
    best_audio_size = 0
    if audio_streams:
        audio_streams.sort(key=lambda x: (x.get('abr') or x.get('tbr') or 0), reverse=True)
        best_audio = audio_streams[0]
        best_audio_size = best_audio.get('filesize') or best_audio.get('filesize_approx') or 0
        if not best_audio_size and duration and (best_audio.get('abr') or best_audio.get('tbr')):
            best_audio_size = int(((best_audio.get('abr') or best_audio.get('tbr')) * 1000 / 8) * duration)

    sizes = {}

    # Audio seul
    if duration:
        sizes['mp3_320'] = int((320 * 1000 / 8) * duration)
    else:
        sizes['mp3_320'] = best_audio_size
    sizes['m4a'] = best_audio_size

    # Vidéo par résolutions
    height_targets = [2160, 1440, 1080, 720, 480, 360]
    for h in height_targets:
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

            total_size = v_size
            if v.get('acodec') == 'none' and best_audio_size:
                total_size += best_audio_size
            sizes[f'{h}p'] = total_size

    # Meilleure qualité max
    video_streams = [f for f in formats if f.get('vcodec') != 'none']
    if video_streams:
        video_streams.sort(key=lambda x: ((x.get('height') or 0), (x.get('tbr') or 0)), reverse=True)
        top = video_streams[0]
        top_size = top.get('filesize') or top.get('filesize_approx') or 0
        if not top_size and duration and top.get('tbr'):
            top_size = int((top.get('tbr') * 1000 / 8) * duration)
        if top.get('acodec') == 'none' and best_audio_size:
            top_size += best_audio_size
        sizes['best'] = top_size
    elif formats:
        f_direct = formats[-1]
        sizes['best'] = f_direct.get('filesize') or f_direct.get('filesize_approx') or data.get('filesize') or data.get('filesize_approx') or 0
    else:
        sizes['best'] = data.get('filesize') or data.get('filesize_approx') or 0

    return sizes


# =============================================================================
# APPLICATION PRINCIPALE
# =============================================================================
class StyveDevDownloadProApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.title("StyveDev Download Pro - Téléchargeur Universel")
        self.geometry("920x840")
        self.minsize(820, 720)
        self.configure(fg_color=THEME["bg_main"])

        # Dossier de sauvegarde par défaut (Téléchargements Windows)
        self.default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        if not os.path.exists(self.default_download_dir):
            self.default_download_dir = os.path.dirname(os.path.abspath(__file__))

        # Variables d'état
        self.destination_dir = ctk.StringVar(value=self.default_download_dir)
        self.status_var = ctk.StringVar(value="✨ Prêt. Collez un lien (YouTube, Facebook, TikTok, Instagram...) pour démarrer.")
        self.stats_var = ctk.StringVar(value="")
        self.platform_var = ctk.StringVar(value="🌐 Prêt")
        self.size_badge_var = ctk.StringVar(value="📦 Taille : En attente d'analyse")
        self.only_single_video_var = ctk.BooleanVar(value=True)

        self.current_video_info = None
        self.current_format_sizes = {}
        self.download_in_progress = False
        self.cancel_requested = False
        self.last_downloaded_file = None
        self.download_history = []

        # Construction de l'interface
        self._build_ui()

    def _build_ui(self):
        # 1. En-tête supérieur
        header_card = ctk.CTkFrame(
            self,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        header_card.pack(fill="x", padx=20, pady=(16, 10))

        header_inner = ctk.CTkFrame(header_card, fg_color="transparent")
        header_inner.pack(fill="x", padx=20, pady=14)

        title_box = ctk.CTkFrame(header_inner, fg_color="transparent")
        title_box.pack(side="left")

        app_title = ctk.CTkLabel(
            title_box,
            text="✨ StyveDev Download Pro",
            font=ctk.CTkFont(size=23, weight="bold"),
            text_color=THEME["text_title"]
        )
        app_title.pack(anchor="w")

        subtitle = ctk.CTkLabel(
            title_box,
            text="Téléchargeur universel haute vitesse • Estimation exacte de la taille avant téléchargement",
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_muted"]
        )
        subtitle.pack(anchor="w", pady=(2, 0))

        controls_box = ctk.CTkFrame(header_inner, fg_color="transparent")
        controls_box.pack(side="right")

        badge = ctk.CTkLabel(
            controls_box,
            text="PRO v3.3",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["badge_version_bg"],
            text_color=THEME["badge_version_text"],
            corner_radius=8,
            padx=10,
            pady=4
        )
        badge.pack(side="right", padx=(10, 0))

        self.theme_menu = ctk.CTkOptionMenu(
            controls_box,
            values=["Sombre", "Clair", "Système"],
            command=self._change_theme,
            width=110,
            height=30,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color=THEME["btn_sec_bg"],
            button_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"]
        )
        self.theme_menu.set("Sombre")
        self.theme_menu.pack(side="right")

        # 2. Zone défilable principale
        scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent", corner_radius=12)
        scroll_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # --- BADGES DES PLATEFORMES SUPPORTÉES ---
        platforms_bar = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=12,
            border_width=1,
            border_color=THEME["card_border"]
        )
        platforms_bar.pack(fill="x", pady=(4, 10))

        p_inner = ctk.CTkFrame(platforms_bar, fg_color="transparent")
        p_inner.pack(fill="x", padx=12, pady=10)

        p_lbl = ctk.CTkLabel(p_inner, text="Plateformes :", font=ctk.CTkFont(size=12, weight="bold"), text_color=THEME["text_muted"])
        p_lbl.pack(side="left", padx=(4, 8))

        for p_name, p_col in PLATFORMS:
            p_badge = ctk.CTkLabel(
                p_inner,
                text=p_name,
                font=ctk.CTkFont(size=11, weight="bold"),
                text_color=p_col,
                fg_color=THEME["badge_bg"],
                corner_radius=8,
                padx=8,
                pady=3
            )
            p_badge.pack(side="left", padx=3)

        # --- SECTION A: SAISIE DU LIEN ---
        input_card = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        input_card.pack(fill="x", pady=8)

        card_title_row = ctk.CTkFrame(input_card, fg_color="transparent")
        card_title_row.pack(fill="x", padx=18, pady=(14, 6))

        in_title = ctk.CTkLabel(
            card_title_row,
            text="Coller le lien de la vidéo ou de l'audio",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_main"]
        )
        in_title.pack(side="left")

        self.platform_badge = ctk.CTkLabel(
            card_title_row,
            textvariable=self.platform_var,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["badge_bg"],
            text_color=THEME["badge_text"],
            corner_radius=6,
            padx=10,
            pady=2
        )
        self.platform_badge.pack(side="right")

        in_row = ctk.CTkFrame(input_card, fg_color="transparent")
        in_row.pack(fill="x", padx=18, pady=(0, 8))

        self.url_entry = ctk.CTkEntry(
            in_row,
            placeholder_text="Collez un lien ici (ex: YouTube, Facebook, TikTok, Instagram, Twitter/X...)",
            height=44,
            font=ctk.CTkFont(size=13),
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            text_color=THEME["text_main"]
        )
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))
        self.url_entry.bind("<KeyRelease>", self._on_url_change)
        self.url_entry.bind("<Return>", lambda e: self.start_analysis())

        clear_btn = ctk.CTkButton(
            in_row,
            text="✕",
            width=36,
            height=44,
            fg_color=THEME["btn_sec_bg"],
            hover_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._clear_url
        )
        clear_btn.pack(side="left", padx=(0, 6))

        paste_btn = ctk.CTkButton(
            in_row,
            text="📋 Coller",
            width=86,
            height=44,
            fg_color=THEME["btn_sec_bg"],
            hover_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self._paste_clipboard
        )
        paste_btn.pack(side="left", padx=(0, 6))

        self.analyze_btn = ctk.CTkButton(
            in_row,
            text="🔍 Analyser",
            width=110,
            height=44,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=THEME["accent_blue"],
            hover_color=THEME["accent_hover"],
            command=self.start_analysis
        )
        self.analyze_btn.pack(side="left")

        security_row = ctk.CTkFrame(input_card, fg_color="transparent")
        security_row.pack(fill="x", padx=18, pady=(0, 12))

        self.single_video_checkbox = ctk.CTkCheckBox(
            security_row,
            text="🔒 Télécharger uniquement cette vidéo (Empêche de télécharger tout le Mix ou la Playlist)",
            variable=self.only_single_video_var,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["checkbox_text"],
            checkbox_height=20,
            checkbox_width=20,
            corner_radius=6
        )
        self.single_video_checkbox.pack(side="left")

        # --- SECTION B: APERÇU VIDÉO & TAILLE EXACTE ---
        self.preview_card = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        self.preview_card.pack(fill="x", pady=8)

        self.preview_placeholder = ctk.CTkLabel(
            self.preview_card,
            text="🎬 Collez un lien ci-dessus pour afficher la vidéo et sa taille exacte avant téléchargement",
            text_color=THEME["text_muted"],
            font=ctk.CTkFont(size=13),
            height=130
        )
        self.preview_placeholder.pack(fill="both", expand=True, padx=20, pady=20)

        self.preview_content = ctk.CTkFrame(self.preview_card, fg_color="transparent")

        self.thumbnail_label = ctk.CTkLabel(self.preview_content, text="", width=220, height=124)
        self.thumbnail_label.pack(side="left", padx=(16, 16), pady=16)

        meta_col = ctk.CTkFrame(self.preview_content, fg_color="transparent")
        meta_col.pack(side="left", fill="both", expand=True, pady=16, padx=(0, 16))

        self.title_label = ctk.CTkLabel(
            meta_col,
            text="Titre du média",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color=THEME["text_main"],
            wraplength=480,
            justify="left",
            anchor="w"
        )
        self.title_label.pack(anchor="w", fill="x")

        self.channel_label = ctk.CTkLabel(
            meta_col,
            text="👤 Auteur : -",
            text_color=THEME["text_muted"],
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        self.channel_label.pack(anchor="w", pady=(4, 0))

        meta_badges_row = ctk.CTkFrame(meta_col, fg_color="transparent")
        meta_badges_row.pack(anchor="w", pady=(8, 0))

        # Badge de la taille exacte calculée
        self.size_badge = ctk.CTkLabel(
            meta_badges_row,
            textvariable=self.size_badge_var,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["badge_size_bg"],
            text_color=THEME["badge_size_text"],
            corner_radius=6,
            padx=10,
            pady=3
        )
        self.size_badge.pack(side="left", padx=(0, 8))

        self.source_badge = ctk.CTkLabel(
            meta_badges_row,
            text="🌐 Plateforme",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["badge_version_bg"],
            text_color=THEME["badge_version_text"],
            corner_radius=6,
            padx=8,
            pady=3
        )
        self.source_badge.pack(side="left", padx=(0, 8))

        self.duration_badge = ctk.CTkLabel(
            meta_badges_row,
            text="⏱️ 00:00",
            font=ctk.CTkFont(size=11),
            fg_color=THEME["badge_bg"],
            text_color=THEME["text_main"],
            corner_radius=6,
            padx=8,
            pady=3
        )
        self.duration_badge.pack(side="left", padx=(0, 8))

        self.views_badge = ctk.CTkLabel(
            meta_badges_row,
            text="👁️ 0 vues",
            font=ctk.CTkFont(size=11),
            fg_color=THEME["badge_bg"],
            text_color=THEME["text_main"],
            corner_radius=6,
            padx=8,
            pady=3
        )
        self.views_badge.pack(side="left")

        # --- SECTION C: FORMAT & DOSSIER ---
        settings_card = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        settings_card.pack(fill="x", pady=8)

        sec_title = ctk.CTkLabel(
            settings_card,
            text="Options de Téléchargement & Destination",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=THEME["text_main"]
        )
        sec_title.pack(anchor="w", padx=18, pady=(14, 8))

        fmt_row = ctk.CTkFrame(settings_card, fg_color="transparent")
        fmt_row.pack(fill="x", padx=18, pady=(0, 10))

        fmt_lbl = ctk.CTkLabel(fmt_row, text="Format / Résolution :", width=160, anchor="w", font=ctk.CTkFont(size=13), text_color=THEME["text_main"])
        fmt_lbl.pack(side="left")

        self.default_format_options = [
            "🎬 Vidéo - Meilleure qualité (Auto / 4K / 1080p)",
            "🎬 Vidéo - 1080p Full HD (MP4)",
            "🎬 Vidéo - 720p HD (MP4)",
            "🎬 Vidéo - 480p SD (MP4)",
            "🎬 Vidéo - 360p Mobile (MP4)",
            "🎵 Audio seul - MP3 Haute Qualité (320 kbps)",
            "🎵 Audio seul - M4A / AAC (Standard)",
            "⚡ Format direct / Source brute"
        ]

        self.format_menu = ctk.CTkOptionMenu(
            fmt_row,
            values=self.default_format_options,
            command=self._on_format_changed,
            height=38,
            font=ctk.CTkFont(size=13),
            dropdown_font=ctk.CTkFont(size=12),
            fg_color=THEME["btn_sec_bg"],
            button_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"]
        )
        self.format_menu.set(self.default_format_options[0])
        self.format_menu.pack(side="left", fill="x", expand=True)

        dest_row = ctk.CTkFrame(settings_card, fg_color="transparent")
        dest_row.pack(fill="x", padx=18, pady=(0, 16))

        dest_lbl = ctk.CTkLabel(dest_row, text="Dossier de destination :", width=160, anchor="w", font=ctk.CTkFont(size=13), text_color=THEME["text_main"])
        dest_lbl.pack(side="left")

        self.dest_entry = ctk.CTkEntry(
            dest_row,
            textvariable=self.destination_dir,
            height=38,
            font=ctk.CTkFont(size=12),
            fg_color=THEME["input_bg"],
            border_color=THEME["input_border"],
            text_color=THEME["text_main"]
        )
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

        browse_btn = ctk.CTkButton(
            dest_row,
            text="📁 Parcourir...",
            width=110,
            height=38,
            fg_color=THEME["btn_sec_bg"],
            hover_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"],
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self._browse_directory
        )
        browse_btn.pack(side="left")

        # --- SECTION D: PROGRESSION & STATISTIQUES ---
        progress_card = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        progress_card.pack(fill="x", pady=8)

        self.status_label = ctk.CTkLabel(
            progress_card,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=THEME["status_color"],
            anchor="w"
        )
        self.status_label.pack(anchor="w", padx=18, pady=(14, 4))

        self.progress_bar = ctk.CTkProgressBar(
            progress_card,
            height=14,
            corner_radius=7,
            progress_color=THEME["accent_blue"],
            fg_color=THEME["progress_track"]
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", padx=18, pady=(4, 6))

        self.stats_label = ctk.CTkLabel(
            progress_card,
            textvariable=self.stats_var,
            font=ctk.CTkFont(size=12),
            text_color=THEME["text_muted"],
            anchor="w"
        )
        self.stats_label.pack(anchor="w", padx=18, pady=(0, 14))

        # --- SECTION E: BOUTONS D'ACTION (AVEC ARRÊT D'URGENCE) ---
        action_row = ctk.CTkFrame(scroll_container, fg_color="transparent")
        action_row.pack(fill="x", pady=(10, 8))

        self.download_btn = ctk.CTkButton(
            action_row,
            text="⚡ TÉLÉCHARGER MAINTENANT",
            height=50,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=THEME["accent_blue"],
            hover_color=THEME["accent_hover"],
            command=self.start_download
        )
        self.download_btn.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.stop_btn = ctk.CTkButton(
            action_row,
            text="🛑 ARRÊTER",
            height=50,
            width=130,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=THEME["accent_danger"],
            hover_color=THEME["accent_danger_hover"],
            command=self.stop_download,
            state="disabled"
        )
        self.stop_btn.pack(side="left", padx=(0, 8))

        self.open_folder_btn = ctk.CTkButton(
            action_row,
            text="📂 Dossier",
            height=50,
            width=120,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=THEME["btn_sec_bg"],
            hover_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"],
            command=self._open_destination_folder,
            state="disabled"
        )
        self.open_folder_btn.pack(side="left")

        # --- SECTION F: HISTORIQUE DE SESSION ---
        history_card = ctk.CTkFrame(
            scroll_container,
            fg_color=THEME["card_bg"],
            corner_radius=14,
            border_width=1,
            border_color=THEME["card_border"]
        )
        history_card.pack(fill="x", pady=(8, 12))

        hist_title_row = ctk.CTkFrame(history_card, fg_color="transparent")
        hist_title_row.pack(fill="x", padx=18, pady=(12, 6))

        hist_lbl = ctk.CTkLabel(
            hist_title_row,
            text="Historique de cette session",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=THEME["text_muted"]
        )
        hist_lbl.pack(side="left")

        self.history_count_lbl = ctk.CTkLabel(
            hist_title_row,
            text="0 fichier téléchargé",
            font=ctk.CTkFont(size=11),
            text_color=THEME["text_muted"]
        )
        self.history_count_lbl.pack(side="right")

        self.history_list_frame = ctk.CTkFrame(history_card, fg_color="transparent")
        self.history_list_frame.pack(fill="x", padx=18, pady=(0, 12))

        self.empty_history_lbl = ctk.CTkLabel(
            self.history_list_frame,
            text="Aucun fichier téléchargé pour le moment dans cette session.",
            text_color=THEME["text_muted"],
            font=ctk.CTkFont(size=12)
        )
        self.empty_history_lbl.pack(anchor="w", pady=4)

    # =========================================================================
    # GESTION DES THÈMES & FORMATS
    # =========================================================================
    def _change_theme(self, choice):
        modes = {"Sombre": "Dark", "Clair": "Light", "Système": "System"}
        mode = modes.get(choice, "Dark")
        ctk.set_appearance_mode(mode)

    def _on_url_change(self, event=None):
        raw_url = self.url_entry.get().strip()
        _, badge_text, badge_color = detect_platform(raw_url)
        self.platform_var.set(badge_text)
        self.platform_badge.configure(text_color=badge_color)

    def _clear_url(self):
        self.url_entry.delete(0, "end")
        self._on_url_change()
        self.status_var.set("Prêt.")
        self.stats_var.set("")
        self.size_badge_var.set("📦 Taille : En attente d'analyse")
        self.format_menu.configure(values=self.default_format_options)
        self.format_menu.set(self.default_format_options[0])

    def _paste_clipboard(self):
        try:
            txt = self.clipboard_get().strip()
            if txt:
                self.url_entry.delete(0, "end")
                self.url_entry.insert(0, txt)
                self._on_url_change()
                self.start_analysis()
        except Exception:
            pass

    def _browse_directory(self):
        chosen = filedialog.askdirectory(initialdir=self.destination_dir.get(), title="Sélectionnez le dossier de sauvegarde")
        if chosen:
            self.destination_dir.set(chosen)

    def _open_destination_folder(self):
        folder = self.destination_dir.get()
        if os.path.exists(folder):
            if sys.platform == "win32":
                os.startfile(folder)
            elif sys.platform == "darwin":
                os.system(f'open "{folder}"')
            else:
                os.system(f'xdg-open "{folder}"')

    def _on_format_changed(self, selected_choice):
        """Met à jour instantanément la taille affichée lors du changement d'option."""
        if not self.current_format_sizes:
            return

        choice = selected_choice.lower()
        size_bytes = 0

        if "1080p" in choice:
            size_bytes = self.current_format_sizes.get('1080p') or self.current_format_sizes.get('best', 0)
        elif "720p" in choice:
            size_bytes = self.current_format_sizes.get('720p') or self.current_format_sizes.get('best', 0)
        elif "480p" in choice:
            size_bytes = self.current_format_sizes.get('480p') or self.current_format_sizes.get('720p', 0)
        elif "360p" in choice:
            size_bytes = self.current_format_sizes.get('360p') or self.current_format_sizes.get('480p', 0)
        elif "mp3" in choice:
            size_bytes = self.current_format_sizes.get('mp3_320', 0)
        elif "m4a" in choice or "aac" in choice:
            size_bytes = self.current_format_sizes.get('m4a', 0)
        else:
            size_bytes = self.current_format_sizes.get('best', 0)

        if size_bytes:
            self.size_badge_var.set(f"📦 Taille exacte : {format_bytes(size_bytes)}")
        else:
            self.size_badge_var.set("📦 Taille : Variable selon flux")

    # =========================================================================
    # ARRÊT D'URGENCE DU TÉLÉCHARGEMENT
    # =========================================================================
    def stop_download(self):
        if self.download_in_progress:
            self.cancel_requested = True
            self.status_var.set("🛑 Arrêt du téléchargement en cours...")
            self.stop_btn.configure(state="disabled", text="Arrêt...")

    # =========================================================================
    # ANALYSE ASYNCHRONE DU LIEN & CALCUL DES TAILLES
    # =========================================================================
    def start_analysis(self):
        raw_url = self.url_entry.get().strip()
        if not raw_url:
            self.status_var.set("⚠️ Veuillez saisir ou coller un lien valide.")
            return

        clean_url = clean_video_url(raw_url, force_single=self.only_single_video_var.get())
        if clean_url != raw_url:
            self.url_entry.delete(0, "end")
            self.url_entry.insert(0, clean_url)

        self._on_url_change()
        plat_name, _, _ = detect_platform(clean_url)

        self.analyze_btn.configure(state="disabled", text="Analyse...")
        self.status_var.set(f"⏳ Analyse du média depuis {plat_name}...")
        self.stats_var.set("Calcul des tailles exactes des fichiers...")
        self.size_badge_var.set("📦 Calcul de la taille...")

        threading.Thread(target=self._analyze_worker, args=(clean_url,), daemon=True).start()

    def _analyze_worker(self, url):
        info = None
        sizes = {}
        error_msg = None

        if HAS_YTDLP:
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'skip_download': True,
                    'extract_flat': False,
                    'noplaylist': True,
                    'playlist_items': '1'
                }
                if FFMPEG_PATH:
                    ydl_opts['ffmpeg_location'] = FFMPEG_PATH

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=False)
                    if 'entries' in data and data['entries']:
                        data = data['entries'][0]

                    # Calcul précis de la taille de chaque format
                    sizes = compute_all_format_sizes(data)

                    info = {
                        'title': data.get('title', 'Titre inconnu'),
                        'uploader': data.get('uploader') or data.get('channel') or data.get('creator') or 'Auteur inconnu',
                        'duration': data.get('duration', 0),
                        'view_count': data.get('view_count', 0),
                        'thumbnail': data.get('thumbnail'),
                        'extractor': data.get('extractor_key') or data.get('extractor', 'Média Web'),
                        'url': url,
                        'sizes': sizes
                    }
            except Exception as e:
                error_msg = str(e)

        # Fallback pour YouTube
        if not info and HAS_PYTUBEFIX and ("youtube.com" in url or "youtu.be" in url):
            try:
                yt = YouTube(url)
                fallback_best_size = 0
                s = yt.streams.get_highest_resolution()
                if s:
                    fallback_best_size = s.filesize

                sizes = {'best': fallback_best_size}

                info = {
                    'title': yt.title or 'Titre YouTube inconnu',
                    'uploader': yt.author or 'Auteur YouTube',
                    'duration': yt.length or 0,
                    'view_count': yt.views or 0,
                    'thumbnail': yt.thumbnail_url,
                    'extractor': 'YouTube',
                    'url': url,
                    'sizes': sizes
                }
            except Exception as e:
                error_msg = str(e)

        self.after(0, self._on_analysis_complete, info, sizes, error_msg)

    def _on_analysis_complete(self, info, sizes, error_msg):
        self.analyze_btn.configure(state="normal", text="🔍 Analyser")

        if not info:
            self.status_var.set("❌ Impossible d'extraire les informations de ce lien.")
            clean_err = error_msg.split("\n")[0] if error_msg else "Vérifiez que le lien est accessible."
            self.stats_var.set(f"Détail : {clean_err[:120]}")
            self.size_badge_var.set("📦 Taille : Erreur d'analyse")
            return

        self.current_video_info = info
        self.current_format_sizes = sizes

        plat_detected, _, _ = detect_platform(info['url'])

        # Taille du meilleur flux
        best_size_str = format_bytes(sizes.get('best', 0))
        self.size_badge_var.set(f"📦 Taille exacte : {best_size_str}")

        self.status_var.set(f"✅ Vidéo détectée : « {info['title'][:50]}... »")
        self.stats_var.set(f"Taille estimée : {best_size_str}  |  Prêt pour téléchargement immédiat.")

        # Mise à jour des libellés du menu avec la taille exacte de chaque choix
        updated_menu_values = []
        fmt_configs = [
            ("🎬 Vidéo - Meilleure qualité (Auto / 4K / 1080p)", sizes.get('best', 0)),
            ("🎬 Vidéo - 1080p Full HD (MP4)", sizes.get('1080p') or sizes.get('best', 0)),
            ("🎬 Vidéo - 720p HD (MP4)", sizes.get('720p') or sizes.get('best', 0)),
            ("🎬 Vidéo - 480p SD (MP4)", sizes.get('480p') or sizes.get('720p', 0)),
            ("🎬 Vidéo - 360p Mobile (MP4)", sizes.get('360p') or sizes.get('480p', 0)),
            ("🎵 Audio seul - MP3 Haute Qualité (320 kbps)", sizes.get('mp3_320', 0)),
            ("🎵 Audio seul - M4A / AAC (Standard)", sizes.get('m4a', 0)),
            ("⚡ Format direct / Source brute", sizes.get('best', 0))
        ]

        for label, b_size in fmt_configs:
            if b_size > 0:
                updated_menu_values.append(f"{label}  [ {format_bytes(b_size)} ]")
            else:
                updated_menu_values.append(label)

        self.format_menu.configure(values=updated_menu_values)
        self.format_menu.set(updated_menu_values[0])

        # Affichage des métadonnées
        self.title_label.configure(text=info['title'])
        self.channel_label.configure(text=f"👤 Créateur / Chaîne : {info['uploader']}")
        self.source_badge.configure(text=f"🌐 {info.get('extractor', plat_detected)}")
        self.duration_badge.configure(text=f"⏱️ {format_duration(info['duration'])}")
        self.views_badge.configure(text=f"👁️ {format_views(info['view_count'])}")

        if info.get('thumbnail'):
            threading.Thread(target=self._load_thumbnail, args=(info['thumbnail'],), daemon=True).start()

        self.preview_placeholder.pack_forget()
        self.preview_content.pack(fill="both", expand=True)

    def _load_thumbnail(self, thumb_url):
        try:
            req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=10) as response:
                img_data = response.read()
            pil_image = Image.open(BytesIO(img_data))
            pil_image.thumbnail((220, 124), Image.Resampling.LANCZOS)
            ctk_img = ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=(pil_image.width, pil_image.height))

            self.after(0, lambda: self.thumbnail_label.configure(image=ctk_img, text=""))
        except Exception:
            pass

    # =========================================================================
    # TÉLÉCHARGEMENT UNIQUE AVEC CONTRÔLE D'ARRÊT
    # =========================================================================
    def start_download(self):
        raw_url = self.url_entry.get().strip()
        if not raw_url:
            self.status_var.set("⚠️ Veuillez coller un lien avant de télécharger.")
            return

        if self.download_in_progress:
            return

        url = clean_video_url(raw_url, force_single=self.only_single_video_var.get())

        out_dir = self.destination_dir.get().strip()
        if not os.path.exists(out_dir):
            try:
                os.makedirs(out_dir, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Dossier invalide", f"Impossible d'accéder au dossier cible :\n{e}")
                return

        format_choice = self.format_menu.get()

        self.download_in_progress = True
        self.cancel_requested = False

        self.download_btn.configure(state="disabled", text="⏳ Téléchargement en cours...", fg_color="#475569")
        self.stop_btn.configure(state="normal", text="🛑 ARRÊTER", fg_color=THEME["accent_danger"])
        self.analyze_btn.configure(state="disabled")
        self.progress_bar.set(0)
        self.status_var.set("🚀 Démarrage du téléchargement...")
        self.stats_var.set("Connexion au serveur multimédia...")

        threading.Thread(target=self._download_worker, args=(url, format_choice, out_dir), daemon=True).start()

    def _download_worker(self, url, format_choice, out_dir):
        success = False
        was_cancelled = False
        error_msg = None
        saved_file = None

        if HAS_YTDLP:
            try:
                ydl_opts = {
                    'outtmpl': os.path.join(out_dir, '%(title).120B [%(id)s].%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'noplaylist': True,
                    'playlist_items': '1',
                    'progress_hooks': [self._ytdlp_progress_hook]
                }

                if FFMPEG_PATH:
                    ydl_opts['ffmpeg_location'] = FFMPEG_PATH

                if "Audio seul - MP3" in format_choice:
                    if FFMPEG_PATH:
                        ydl_opts['format'] = 'bestaudio/best'
                        ydl_opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '320',
                        }]
                    else:
                        ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
                elif "Audio seul - M4A" in format_choice:
                    ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio/best'
                elif "1080p" in format_choice:
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "720p" in format_choice:
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "480p" in format_choice:
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "360p" in format_choice:
                    ydl_opts['format'] = 'bestvideo[height<=360]+bestaudio/best[height<=360]/best'
                    ydl_opts['merge_output_format'] = 'mp4'
                elif "Format direct" in format_choice:
                    ydl_opts['format'] = 'best'
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                    ydl_opts['merge_output_format'] = 'mp4'

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    data = ydl.extract_info(url, download=True)
                    if 'entries' in data and data['entries']:
                        data = data['entries'][0]

                    saved_file = ydl.prepare_filename(data)
                    if "Audio seul - MP3" in format_choice and FFMPEG_PATH:
                        saved_file = os.path.splitext(saved_file)[0] + ".mp3"

                success = True

            except Exception as e:
                if "CANCELLED_BY_USER" in str(e):
                    was_cancelled = True
                else:
                    error_msg = str(e)

        if not success and not was_cancelled and HAS_PYTUBEFIX and ("youtube.com" in url or "youtu.be" in url):
            try:
                self.after(0, lambda: self.status_var.set("Bascule vers le moteur secondaire..."))

                def on_pytube_progress(stream, chunk, bytes_remaining):
                    if self.cancel_requested:
                        raise Exception("CANCELLED_BY_USER")
                    total = stream.filesize
                    downloaded = total - bytes_remaining
                    pct = downloaded / total
                    self.after(0, self._update_progress, pct, f"⚡ Téléchargement : {int(pct*100)}%", f"{format_bytes(downloaded)} / {format_bytes(total)}")

                yt = YouTube(url, on_progress_callback=on_pytube_progress)
                if "Audio seul" in format_choice:
                    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
                else:
                    stream = yt.streams.get_highest_resolution() or yt.streams.filter(type="video").order_by("resolution").desc().first()

                saved_file = stream.download(output_path=out_dir)
                success = True
            except Exception as e:
                if "CANCELLED_BY_USER" in str(e):
                    was_cancelled = True
                else:
                    error_msg = str(e)

        if was_cancelled:
            self._cleanup_temp_files(out_dir)

        self.after(0, self._on_download_complete, success, was_cancelled, error_msg, saved_file)

    def _ytdlp_progress_hook(self, d):
        if self.cancel_requested:
            raise Exception("CANCELLED_BY_USER")

        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            downloaded = d.get('downloaded_bytes', 0)
            speed = d.get('speed') or 0
            eta = d.get('eta') or 0

            percent = (downloaded / total) if total > 0 else 0
            speed_str = f"{format_bytes(speed)}/s" if speed else "-- Mo/s"
            size_str = f"{format_bytes(downloaded)} / {format_bytes(total)}" if total else format_bytes(downloaded)
            eta_str = f"⏳ Restant : {format_duration(eta)}" if eta else ""

            status_msg = f"⚡ Téléchargement en cours : {int(percent * 100)}%"
            stats_msg = f"Vitesse : {speed_str}  |  Taille : {size_str}  |  {eta_str}"

            self.after(0, self._update_progress, percent, status_msg, stats_msg)

        elif d['status'] == 'finished':
            self.after(0, self._update_progress, 1.0, "🔧 Assemblage et conversion FFmpeg...", "Finalisation du fichier...")

    def _update_progress(self, percent, status_msg, stats_msg):
        self.progress_bar.set(percent)
        self.status_var.set(status_msg)
        self.stats_var.set(stats_msg)

    def _cleanup_temp_files(self, out_dir):
        try:
            for part in glob.glob(os.path.join(out_dir, "*.part")):
                try:
                    os.remove(part)
                except Exception:
                    pass
            for ytdl in glob.glob(os.path.join(out_dir, "*.ytdl")):
                try:
                    os.remove(ytdl)
                except Exception:
                    pass
        except Exception:
            pass

    def _on_download_complete(self, success, was_cancelled, error_msg, saved_file):
        self.download_in_progress = False
        self.cancel_requested = False

        self.download_btn.configure(
            state="normal",
            text="⚡ TÉLÉCHARGER MAINTENANT",
            fg_color=THEME["accent_blue"]
        )
        self.stop_btn.configure(state="disabled", text="🛑 ARRÊTER", fg_color=THEME["accent_danger"])
        self.analyze_btn.configure(state="normal")

        if was_cancelled:
            self.progress_bar.set(0)
            self.status_var.set("🛑 Téléchargement arrêté avec succès.")
            self.stats_var.set("Le téléchargement a été interrompu et les fichiers temporaires nettoyés.")
            return

        if success:
            self.last_downloaded_file = saved_file
            self.progress_bar.set(1.0)
            self.status_var.set("🎉 Téléchargement terminé avec succès !")
            file_name = os.path.basename(saved_file) if saved_file else "Fichier enregistré"
            self.stats_var.set(f"Fichier : {file_name}")
            self.open_folder_btn.configure(state="normal")

            self._add_to_history(saved_file)

            messagebox.showinfo(
                "Téléchargement réussi",
                f"Votre média a été téléchargé avec succès !\n\nNom : {file_name}\nDossier : {self.destination_dir.get()}"
            )
        else:
            self.status_var.set("❌ Échec du téléchargement.")
            clean_err = error_msg.split("\n")[0] if error_msg else "Erreur de connexion ou média privé."
            self.stats_var.set(f"Raison : {clean_err[:120]}")
            messagebox.showerror(
                "Erreur de téléchargement",
                f"Le téléchargement n'a pas pu aboutir :\n\n{clean_err}\n\nVérifiez que le lien est accessible publiquement."
            )

    def _add_to_history(self, file_path):
        if not file_path:
            return
        if self.empty_history_lbl.winfo_ismapped():
            self.empty_history_lbl.pack_forget()

        self.download_history.append(file_path)
        count = len(self.download_history)
        self.history_count_lbl.configure(text=f"{count} fichier{'s' if count > 1 else ''} téléchargé{'s' if count > 1 else ''}")

        file_name = os.path.basename(file_path)

        item_row = ctk.CTkFrame(self.history_list_frame, fg_color=THEME["hist_item_bg"], corner_radius=8)
        item_row.pack(fill="x", pady=3)

        icon_lbl = ctk.CTkLabel(item_row, text="✅", width=26)
        icon_lbl.pack(side="left", padx=(10, 6), pady=8)

        name_lbl = ctk.CTkLabel(
            item_row,
            text=file_name,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=THEME["hist_item_text"],
            anchor="w"
        )
        name_lbl.pack(side="left", fill="x", expand=True)

        play_btn = ctk.CTkButton(
            item_row,
            text="▶️ Ouvrir",
            width=70,
            height=28,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color=THEME["btn_sec_bg"],
            hover_color=THEME["btn_sec_hover"],
            text_color=THEME["btn_sec_text"],
            command=lambda f=file_path: os.startfile(f) if sys.platform == "win32" and os.path.exists(f) else None
        )
        play_btn.pack(side="right", padx=(4, 10), pady=6)


# =============================================================================
# EXÉCUTION
# =============================================================================
def main():
    app = StyveDevDownloadProApp()
    app.mainloop()


if __name__ == "__main__":
    main()