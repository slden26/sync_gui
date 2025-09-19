import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os, shutil, datetime, json

SETTINGS_FILE = "settings.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                source_entry.insert(0, data.get("source", ""))
                target_entry.insert(0, data.get("target", ""))
                mode_var.set(data.get("mode", "overwrite"))
        except Exception:
            pass

def save_settings():
    data = {
        "source": source_entry.get(),
        "target": target_entry.get(),
        "mode": mode_var.get()
    }
    try:
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def choose_source():
    path = filedialog.askdirectory()
    if path:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, path)

def choose_target():
    path = filedialog.askdirectory()
    if path:
        target_entry.delete(0, tk.END)
        target_entry.insert(0, path)

def start_sync():
    global file_list, total_files, copied_files
    src = source_entry.get()
    dst = target_entry.get()
    mode = mode_var.get()

    if not src or not dst:
        messagebox.showerror("Ошибка", "Укажите обе папки.")
        return

    save_settings()

    file_list = []
    for root, _, files in os.walk(src):
        for file in files:
            file_list.append((root, file))
    total_files = len(file_list)
    copied_files = 0
    progress_bar["maximum"] = total_files
    sync_step(src, dst, mode)

def sync_step(src, dst, mode):
    global copied_files
    if copied_files >= total_files:
        messagebox.showinfo("Готово", "Синхронизация завершена.")
        return

    root_dir, file = file_list[copied_files]
    rel_path = os.path.relpath(root_dir, src)
    target_dir = os.path.join(dst, rel_path)
    os.makedirs(target_dir, exist_ok=True)

    src_file = os.path.join(root_dir, file)
    dst_file = os.path.join(target_dir, file)

    if os.path.exists(dst_file):
        if mode == "overwrite":
            shutil.copy2(src_file, dst_file)
        elif mode == "rename":
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name, ext = os.path.splitext(file)
            new_name = f"{name}_{timestamp}{ext}"
            dst_file = os.path.join(target_dir, new_name)
            shutil.copy2(src_file, dst_file)
    else:
        shutil.copy2(src_file, dst_file)

    copied_files += 1
    progress_bar["value"] = copied_files
    root.after(1, lambda: sync_step(src, dst, mode))

root = tk.Tk()
root.title("Синхронизация папок")
root.geometry("580x250")

try:
    root.iconbitmap("icon.ico")  # ← подключение иконки
except Exception:
    pass

tk.Label(root, text="Исходная папка").grid(row=0, column=0, padx=10, pady=5, sticky="w")
source_entry = tk.Entry(root, width=50)
source_entry.grid(row=0, column=1)
tk.Button(root, text="Обзор", command=choose_source).grid(row=0, column=2)

tk.Label(root, text="Целевая папка").grid(row=1, column=0, padx=10, pady=5, sticky="w")
target_entry = tk.Entry(root, width=50)
target_entry.grid(row=1, column=1)
tk.Button(root, text="Обзор", command=choose_target).grid(row=1, column=2)

mode_var = tk.StringVar(value="overwrite")
tk.Label(root, text="При конфликте:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Radiobutton(root, text="Перезаписать", variable=mode_var, value="overwrite").grid(row=2, column=1, sticky="w")
tk.Radiobutton(root, text="Сохранять с датой", variable=mode_var, value="rename").grid(row=3, column=1, sticky="w")

progress_bar = ttk.Progressbar(root, length=400)
progress_bar.grid(row=4, column=1, pady=15)

tk.Button(root, text="Синхронизировать", command=start_sync).grid(row=5, column=1, pady=10)

load_settings()
root.mainloop()