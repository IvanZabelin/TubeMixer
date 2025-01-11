import os
from yt_dlp import YoutubeDL


def download_youtube_shorts(
        query, max_videos, output_folder, progress_var, root
        ):
    os.makedirs(output_folder, exist_ok=True)
    search_url = f"ytsearch{max_videos}:{query} shorts"

    ydl_opts = {
        'nocache': True,
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'format': 'best',
        'quiet': False,
        'progress_hooks': [lambda d: update_progress(d, progress_var, root)]
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(search_url, download=True)
            videos_downloaded = len(info_dict.get('entries', []))
            print(f"Скачано {videos_downloaded} видео в папку {output_folder}")
    except Exception as e:
        print(f"Ошибка при скачивании: {e}")


def update_progress(d, progress_var, root):
    """Функция обновления прогресса в tkinter."""
    if d['status'] == 'downloading':
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 0)
        if total > 0:
            progress_var.set((downloaded / total) * 100)
            root.update_idletasks()
    elif d['status'] == 'finished':
        progress_var.set(100)
        root.update_idletasks()
