import json
import tkinter as tk
from tkinter import filedialog

class FolderSelector(tk.Frame):
    def __init__(self, master, label_text, file_type="directory", entry_width=20, variable=None):
        super().__init__(master)
        self.label_text = label_text
        self.file_type = file_type
        self.config_file = "config.json"
        self.entry_width = entry_width
        self.variable = variable
        self.build_ui()

    def build_ui(self):
        self.label = tk.Label(self, text=self.label_text)
        self.label.pack(side=tk.LEFT)

        self.entry = tk.Entry(self, width=self.entry_width, textvariable=self.variable)
        self.entry.pack(side=tk.LEFT)
        self.load_config()

        self.button = tk.Button(self, text="选择目录" if self.file_type == "directory" else "选择文件", command=self.select_folder)
        self.button.pack(side=tk.LEFT)

    def select_folder(self):
        if self.file_type == "directory":
            folder_path = filedialog.askdirectory()
        else:
            folder_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")])
        if folder_path:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, folder_path)
            self.master.master.log_text.insert(tk.END, f"{self.label_text}: {folder_path}\n")
            self.save_config(folder_path)

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                config_data = json.load(f)
                folder_path = config_data.get(self.label_text, "")
                if folder_path:
                    self.entry.delete(0, tk.END)
                    self.entry.insert(0, folder_path)
        except FileNotFoundError:
            pass

    def save_config(self, folder_path):
        try:
            with open(self.config_file, "r") as f:
                config_data = json.load(f)

            config_data[self.label_text] = folder_path

            with open(self.config_file, "w") as f:
                json.dump(config_data, f, indent=2)
        except FileNotFoundError:
            pass
