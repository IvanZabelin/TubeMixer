import os
import random
from moviepy.editor import VideoFileClip, concatenate_videoclips


def compile_videos(input_folder, output_file, target_duration, progress_var=None, root=None):
    """
    Создает компиляцию видео из папки с учетом целевой длительности. Если длительность недостаточна, видео дублируются.

    :param input_folder: Папка с входными видео
    :param output_file: Путь для выходного файла
    :param target_duration: Целевая длительность итогового видео (в секундах)
    :param progress_var: Переменная прогресса для обновления (опционально)
    :param root: Tkinter root для обновления UI (опционально)
    """
    # Получение всех видеофайлов из папки
    video_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f)) and f.endswith(('.mp4', '.avi', '.mov'))
    ]

    if not video_files:
        raise ValueError("В папке нет подходящих видеофайлов.")

    # Случайное перемешивание видео
    random.shuffle(video_files)

    # Список видеоклипов для компиляции
    clips = []
    total_duration = 0.0

    while total_duration < target_duration:
        for video_file in video_files:
            try:
                # Загружаем видеоклип
                clip = VideoFileClip(video_file)
                duration = clip.duration

                # Обрезка видео по необходимости
                if total_duration + duration > target_duration:
                    duration_to_cut = target_duration - total_duration
                    clip = clip.subclip(0, duration_to_cut)

                clips.append(clip)
                total_duration += clip.duration

                # Обновление прогресса
                if progress_var and root:
                    progress_percentage = (total_duration / target_duration) * 100
                    progress_var.set(min(progress_percentage, 100))
                    root.update_idletasks()

                if total_duration >= target_duration:
                    break

            except Exception as e:
                print(f"Ошибка при обработке файла {video_file}: {e}")

        # Если все видео использованы, перемешиваем их заново
        random.shuffle(video_files)

    # Объединяем клипы
    final_clip = concatenate_videoclips(clips, method="compose")

    # Сохраняем итоговое видео
    final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", threads=4)

    # Завершение прогресса
    if progress_var and root:
        progress_var.set(100)
        root.update_idletasks()

    print(f"Видео успешно создано: {output_file}")
