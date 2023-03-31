import tkinter as tk
from top_frame import TopFrame
from middle_frame import MiddleFrame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x800")
        self.title("Cocos自动打包工具")
        self.build_ui()

    def build_ui(self):
        self.top_frame = TopFrame(self)
        self.top_frame.pack(fill=tk.X)

        self.middle_frame = MiddleFrame(self)
        self.middle_frame.pack(side="top", fill="x")

        self.log_frame = tk.Frame(self)
        self.log_frame.pack(side=tk.BOTTOM, pady=50)

        self.log_text = tk.Text(self.log_frame, width=100, height=20)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text.config(yscrollcommand=self.scrollbar.set)

    def update_log_text(self, line):
        self.log_text.insert(tk.END, line)
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

        # 保留最多100行日志
        max_lines = 100
        line_count = int(self.log_text.index('end-1c').split('.')[0])

        if line_count > max_lines:
            self.log_text.delete(1.0, float(line_count - max_lines))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
