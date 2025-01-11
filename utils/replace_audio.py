"""Програмка для замены музыки в видео файлах."""
import os
import random


def replace_audio_in_video(video_path, audio_path, output_path):
    try:
        from moviepy.audio.io.AudioFileClip import AudioFileClip
        from moviepy.video.io.VideoFileClip import VideoFileClip

        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)

        if audio.duration < video.duration:
            print(f"⚠️ Аудио ({audio.duration:.2f}s) короче видео ({video.duration:.2f}s).")
            audio = audio.audio_loop(duration=video.duration)

        video_with_new_audio = video.set_audio(audio)
        video_with_new_audio.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            threads=4
        )

        video.close()
        audio.close()

    except Exception as e:
        print(f"Ошибка при обработке {video_path} с аудио {audio_path}: {e}")


def replace_audio_in_folder(
        video_folder, audio_folder, output_folder, progress_var=None, root=None
        ):
    os.makedirs(output_folder, exist_ok=True)

    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.mov', '.avi'))]
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav', '.aac'))]

    for video_file in video_files:
        audio_file = random.choice(audio_files)
        video_path = os.path.join(video_folder, video_file)
        audio_path = os.path.join(audio_folder, audio_file)
        output_path = os.path.join(output_folder, f"new_{video_file}")

        replace_audio_in_video(video_path, audio_path, output_path)

    if progress_var and root:
        progress_var.set(100)
        root.update_idletasks()
    print("Замена музыки завершена!")
