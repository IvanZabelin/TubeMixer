"""Програмка для замены музыки в видео файлах."""
import os
import random
from moviepy.editor import VideoFileClip, AudioFileClip
import tkinter as tk
from tkinter import filedialog


root = tk.Tk()
root.withdraw()

VIDEO_FOLDER = filedialog.askdirectory(title="Выберите папку с видео")
AUDIO_FOLDER = filedialog.askdirectory(title="Выберите папку с аудио")
OUTPUT_FOLDER = filedialog.askdirectory(title="Выберите папку для вывода")


os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def replace_audio_in_video(video_path, audio_path, output_path):
    video_clip = VideoFileClip(video_path)
    audio_clip = AudioFileClip(audio_path)

    audio_clip = audio_clip.subclip(0, video_clip.duration)
    video_with_new_audio = video_clip.set_audio(audio_clip)
    video_with_new_audio.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        threads=4,
    )


video_files = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(('.mp4', '.mov', '.avi'))]
audio_files = [f for f in os.listdir(AUDIO_FOLDER) if f.endswith(('.mp3', '.wav', '.aac'))]
for video_file in video_files:
    audio_file = random.choice(audio_files)

    video_path = os.path.join(VIDEO_FOLDER, video_file)
    audio_path = os.path.join(AUDIO_FOLDER, audio_file)

    output_path = os.path.join(OUTPUT_FOLDER, f"new_{video_file}")

    replace_audio_in_video(video_path, audio_path, output_path)

print("Готово!")
