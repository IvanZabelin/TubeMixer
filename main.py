import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER, INFO, WARNING
from tkinter import filedialog, simpledialog, messagebox
from utils.download import download_youtube_shorts
from utils.replace_audio import replace_audio_in_folder
from utils.compile_videos import compile_videos, compile_random_clips


def ask_directory(title: str):
    """Запрашивает у пользователя путь к директории."""
    path = filedialog.askdirectory(title=title)
    return path or None


def ask_integer(title: str, prompt: str, minvalue: int = 1):
    """Запрашивает целое число у пользователя."""
    result = simpledialog.askinteger(title, prompt, minvalue=minvalue)
    if result is None:
        messagebox.showerror("Ошибка", "Введите корректное число.")
    return result


def reset_progress(progress_var, root):
    """Сбрасывает прогресс-бар."""
    progress_var.set(0)
    root.update_idletasks()

def replace_audio_action(progress_var, root):
    reset_progress(progress_var, root)

    video_folder = ask_directory("Выберите папку с видео")
    if not video_folder:
        return

    audio_folder = ask_directory("Выберите папку с аудио")
    if not audio_folder:
        return

    output_folder = ask_directory("Выберите папку для сохранения")
    if not output_folder:
        return

    replace_audio_in_folder(video_folder, audio_folder, output_folder, progress_var, root)
    messagebox.showinfo("Готово", "Замена музыки завершена!")

    reset_progress(progress_var, root)


def download_shorts_action(progress_var, root):
    reset_progress(progress_var, root)

    query = simpledialog.askstring("Запрос", "Введите ключевое слово для поиска:")
    if not query:
        return

    max_videos = ask_integer("Количество видео", "Введите количество видео для скачивания:")
    if max_videos is None:
        return

    output_folder = ask_directory("Выберите папку для сохранения шортсов")
    if not output_folder:
        return

    downloaded = download_youtube_shorts(query, max_videos, output_folder, progress_var, root)
    messagebox.showinfo("Готово", f"Скачано {downloaded} из {max_videos} видео.")

    reset_progress(progress_var, root)


def create_compilation_action(progress_var, root):
    reset_progress(progress_var, root)

    input_folder = ask_directory("Выберите папку с короткими видео")
    if not input_folder:
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        return

    target_duration = ask_integer(
        "Длительность ролика",
        "Введите желаемую длительность итогового видео (в секундах):",
    )
    if target_duration is None:
        return

    compile_videos(input_folder, output_file, target_duration, progress_var, root)
    messagebox.showinfo("Готово", "Компиляция создана!")

    reset_progress(progress_var, root)


def create_random_clips_compilation_action(progress_var, root):
    reset_progress(progress_var, root)

    input_folder = ask_directory("Выберите папку с короткими видео")
    if not input_folder:
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
    if not output_file:
        return

    try:
        num_videos = ask_integer("Количество роликов", "Введите количество роликов для создания:")
        if num_videos is None:
            return

        target_duration = ask_integer(
            "Длительность ролика",
            "Введите желаемую длительность каждого ролика (в секундах):",
        )
        if target_duration is None:
            return

        compile_random_clips(
            input_folder,
            output_file,
            num_videos,
            target_duration,
            progress_var=progress_var,
            root=root,
        )
        messagebox.showinfo("Готово", f"Создано {num_videos} роликов!")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))
    finally:
        reset_progress(progress_var, root)


def main_menu():
    app = ttk.Window(themename="superhero")
    app.title("TubeMixer Utility")
    app.geometry("600x600")
    app.resizable(False, False)

    # Заголовок
    title_label = ttk.Label(
        app, 
        text="TubeMixer", 
        font=("Arial", 20, "bold"), 
        bootstyle=PRIMARY
    )
    title_label.pack(pady=20)

    # Описание
    subtitle_label = ttk.Label(
        app, 
        text="Выберите действие ниже", 
        font=("Arial", 12), 
        bootstyle=INFO
    )
    subtitle_label.pack(pady=10)

    # Прогресс-бар
    progress_var = ttk.DoubleVar()
    progress = ttk.Progressbar(app, variable=progress_var, maximum=100, length=420)
    progress.pack(pady=20)

    # Кнопки действий
    download_shorts_btn = ttk.Button(
        app,
        text="Скачать шортсы с YouTube",
        command=lambda: download_shorts_action(progress_var, app),
        bootstyle=PRIMARY,
        width=50
    )
    download_shorts_btn.pack(pady=10)

    replace_audio_btn = ttk.Button(
        app,
        text="Заменить музыку в видео",
        command=lambda: replace_audio_action(progress_var, app),
        bootstyle=SUCCESS,
        width=50
    )
    replace_audio_btn.pack(pady=10)

    create_compilation_btn = ttk.Button(
        app,
        text="Создать компиляцию видео",
        command=lambda: create_compilation_action(progress_var, app),
        bootstyle=DANGER,
        width=50
    )
    create_compilation_btn.pack(pady=10)

    random_clips_compilation_btn = ttk.Button(
        app,
        text="Создать компиляцию случайных клипов",
        command=lambda: create_random_clips_compilation_action(progress_var, app),
        bootstyle=WARNING,
        width=50
    )
    random_clips_compilation_btn.pack(pady=10)

    # Футер
    footer_label = ttk.Label(
        app,
        text="© 2025 TubeMixer",
        font=("Arial", 10),
        bootstyle=INFO
    )
    footer_label.pack(side="bottom", pady=10)

    app.mainloop()


if __name__ == "__main__":
    main_menu()
