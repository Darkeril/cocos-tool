import tkinter as tk
from folder_selector import FolderSelector

class TopFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build_ui()

    def build_ui(self):
        self.canvas = tk.Canvas(self, bg='white')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window(0, 0, window=self.inner_frame, anchor='nw')

        self.label_title = tk.Label(self.inner_frame, text="配置", font=("Arial", 14), bg='white')
        self.label_title.pack(side=tk.TOP, pady=10, anchor=tk.W)

        self.var_cocos_creator_path = tk.StringVar()
        self.var_cocos_pro_root = tk.StringVar()
        self.var_cocos_hot_root = tk.StringVar()
        self.var_major_version = tk.StringVar()
        self.var_minor_version = tk.StringVar()

        self.folder_selector = FolderSelector(self.inner_frame, "CocosCreatorPath", file_type="file", entry_width=60, variable=self.var_cocos_creator_path)
        self.folder_selector.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)

        self.folder_selector = FolderSelector(self.inner_frame, "CocosProRoot", file_type="directory", entry_width=60, variable=self.var_cocos_pro_root)
        self.folder_selector.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)

        self.folder_selector = FolderSelector(self.inner_frame, "CocosHotRoot", file_type="directory", entry_width=60, variable=self.var_cocos_hot_root)
        self.folder_selector.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)

        version_frame = tk.Frame(self.inner_frame, bg='white')
        version_frame.pack(side=tk.TOP, padx=10, pady=5, anchor=tk.W)

        tk.Label(version_frame, text='打包大版本号: ', bg='white').pack(side=tk.LEFT)
        self.major_version_entry = tk.Entry(version_frame, textvariable=self.var_major_version)
        self.major_version_entry.pack(side=tk.LEFT)

        tk.Label(version_frame, text='打包小版本号: ', bg='white').pack(side=tk.LEFT)
        self.minor_version_entry = tk.Entry(version_frame, textvariable=self.var_minor_version)
        self.minor_version_entry.pack(side=tk.LEFT)

        self.inner_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        self.canvas.bind('<Configure>', self.on_canvas_configure)


    def on_canvas_configure(self, event):
        self.canvas.config(width=event.width)
