import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, DANGER, INFO
from tkinter import filedialog, simpledialog, messagebox
from utils.donwnload import download_youtube_shorts
from utils.replace_audio import replace_audio_in_folder
from utils.compile_videos import compile_videos

def replace_audio_action(progress_var, root):
    video_folder = filedialog.askdirectory(title="Выберите папку с видео")
    if not video_folder:
        return

    audio_folder = filedialog.askdirectory(title="Выберите папку с аудио")
    if not audio_folder:
        return

    output_folder = filedialog.askdirectory(
        title="Выберите папку для сохранения"
    )
    if not output_folder:
        return

    replace_audio_in_folder(video_folder, audio_folder, output_folder, progress_var, root)
    messagebox.showinfo("Готово", "Замена музыки завершена!")

    # Сброс прогресса после завершения
    progress_var.set(0)
    root.update_idletasks()


def download_shorts_action(progress_var, root):
    query = simpledialog.askstring(
        "Запрос", "Введите ключевое слово для поиска:" 
    )
    if not query:
        return

    try:
        max_videos = simpledialog.askinteger(
            "Количество видео", "Введите количество видео для скачивания:",
            minvalue=1,
        )
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число.")
        return

    output_folder = filedialog.askdirectory(
        title="Выберите папку для сохранения шортсов"
    )
    if not output_folder:
        return

    # Запуск скачивания с прогрессом
    download_youtube_shorts(query, max_videos, output_folder, progress_var, root)
    messagebox.showinfo("Готово", f"Скачано {max_videos} видео!")

    # Сброс прогресса после завершения
    progress_var.set(0)
    root.update_idletasks()


def create_compilation_action(progress_var, root):
    input_folder = filedialog.askdirectory(
        title="Выберите папку с короткими видео"
    )
    if not input_folder:
        return

    output_file = filedialog.asksaveasfilename(
        defaultextension=".mp4",
        filetypes=[("MP4 files", "*.mp4")]
    )
    if not output_file:
        return

    try:
        target_duration = simpledialog.askinteger(
            "Длительность ролика",
            "Введите желаемую длительность итогового видео (в секундах):",
            minvalue=1
        )
    except ValueError:
        messagebox.showerror("Ошибка", "Введите корректное число.")
        return

    # Запуск создания компиляции с прогрессом
    compile_videos(input_folder, output_file, target_duration, progress_var, root)
    messagebox.showinfo("Готово", "Компиляция создана!")

    # Сброс прогресса после завершения
    progress_var.set(0)
    root.update_idletasks()


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

    # Футер
    footer_label = ttk.Label(
        app,
        text="© 2025 TubeMixer Team",
        font=("Arial", 10),
        bootstyle=INFO
    )
    footer_label.pack(side="bottom", pady=10)

    app.mainloop()


if __name__ == "__main__":
    main_menu()
