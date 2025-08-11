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

def compile_random_clips(input_folder, output_file, num_videos, target_duration, min_duration=5, max_duration=8, progress_var=None, root=None):
    video_files = [
        os.path.join(input_folder, f) for f in os.listdir(input_folder)
        if os.path.isfile(os.path.join(input_folder, f)) and f.endswith(('.mp4', '.avi', '.mov'))
    ]

    if not video_files:
        raise ValueError("В папке нет подходящих видеофайлов.")

    total_steps = num_videos
    for n in range(num_videos):
        print(f"Создание ролика {n+1} из {num_videos}")
        base, ext = os.path.splitext(output_file)
        current_output = f"{base}_{n+1}{ext}"

        subclips = []
        total_duration_current = 0.0
        original_clips = []
        max_attempts = 100

        attempt = 0
        while total_duration_current < target_duration and attempt < max_attempts:
            video_file = random.choice(video_files)
            try:
                clip = VideoFileClip(video_file)
                original_clips.append(clip)
                T = clip.duration

                if T < min_duration:
                    continue

                if total_duration_current + min_duration > target_duration:
                    D = target_duration - total_duration_current
                    if D <= 0 or D > T:
                        continue
                    S = random.uniform(0, T - D) if T - D > 0 else 0
                    subclip = clip.subclip(S, S + D)
                    subclips.append(subclip)
                    total_duration_current += D
                    break
                else:
                    D = random.uniform(min_duration, min(max_duration, T))
                    if D > T:
                        continue
                    S = random.uniform(0, T - D) if T - D > 0 else 0
                    subclip = clip.subclip(S, S + D)
                    subclips.append(subclip)
                    total_duration_current += D

            except Exception as e:
                print(f"Ошибка при обработке файла {video_file}: {e}")
            finally:
                attempt += 1

        if not subclips:
            print(f"Предупреждение: Не удалось создать ролик {n+1} с продолжительностью {target_duration} секунд.")
            continue

        random.shuffle(subclips)
        final_clip = concatenate_videoclips(subclips, method="compose")

        print(f"Итоговая длительность ролика {n+1}: {final_clip.duration:.2f} секунд")

        final_clip.write_videofile(
            current_output,
            codec="libx264",
            audio_codec="aac",
            threads=4,
            fps=30  # фиксируем FPS
        )

        for clip in original_clips:
            clip.close()

        if progress_var and root:
            progress_value = (n + 1) / total_steps * 100
            print(f"Обновление прогресса: {progress_value:.2f}%")
            progress_var.set(progress_value)
            root.update_idletasks()

        print(f"✅ Создан ролик: {current_output}")
