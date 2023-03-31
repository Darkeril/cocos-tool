import os
import subprocess
import tkinter as tk
import threading
import codecs

class MiddleFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.build_ui()

    def build_ui(self):
        self.label_title = tk.Label(self, text="功能", font=("Arial", 14))
        self.label_title.grid(row=0, column=0, columnspan=2, pady=10)

        self.button_test_package = tk.Button(self, text="打测试包", command=self.start_execute_build_dev)
        self.button_test_package.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.button_test_hot_package = tk.Button(self, text="打测试热更新差异包")
        self.button_test_hot_package.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.button_official_package = tk.Button(self, text="打正式包")
        self.button_official_package.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.button_official_hot_package = tk.Button(self, text="打正式包热更新差异包")
        self.button_official_hot_package.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def start_execute_build_dev(self):
        # 创建新线程并启动
        build_dev_thread = threading.Thread(target=self.execute_build_dev)
        build_dev_thread.start()

    def execute_build_dev(self):
        cocos_creator_path = self.master.top_frame.var_cocos_creator_path.get()
        cocos_pro_root = self.master.top_frame.var_cocos_pro_root.get()

        self.changeVersion()

        bat_file = "build_dev.bat"

        if os.path.exists(bat_file):
            # 使用非阻塞方式执行命令
            process = subprocess.Popen([bat_file, cocos_creator_path, cocos_pro_root], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)

            # 实时读取输出并添加到log框
            while True:
                try:
                    output = process.stdout.readline()
                    if output == '' and process.poll() is not None:
                        break
                    if output != '':
                        self.master.update_log_text(output)

                except UnicodeDecodeError:
                    pass

            # 获取进程的返回值
            returncode = process.wait()

            if returncode == 0:
                self.master.update_log_text("打包成功！\n")
                self.changeVersionRollback()
            else:
                self.master.update_log_text(f"打包失败，错误码：{returncode}\n")
        else:
            self.master.update_log_text(f"错误：找不到 {bat_file}\n")

    def update_log_text(self, process):
        try:
            # 实时读取输出并添加到log框
            for line in iter(process.stdout.readline, ""):
                self.master.update_log_text(line)

            # 实时读取错误输出并添加到log框
            for line in iter(process.stderr.readline, ""):
                self.master.update_log_text(line)

        except UnicodeDecodeError:
            pass

    def changeVersion(self):
        # 获取 var_big_version 和 var_small_version 的值
        big_version = self.master.top_frame.var_major_version.get()
        small_version = self.master.top_frame.var_minor_version.get()

        cocos_pro_root = self.master.top_frame.var_cocos_pro_root.get()
        with open(cocos_pro_root + '/assets/src/constant/VersionConstant.ts', 'r', encoding='utf-8') as f:
            ts_file = f.read()

        ts_file = ts_file.replace('export let bigVersion: number = null;', f'export let bigVersion: number = {big_version};')
        ts_file = ts_file.replace('export let smallVersion: string = null;', f'export let smallVersion: string = "{small_version}";')

        with open(cocos_pro_root + '/assets/src/constant/VersionConstant.ts', 'w', encoding='utf-8') as f:
            f.write(ts_file)

    def changeVersionRollback(self):
        # 获取 var_big_version 和 var_small_version 的值
        big_version = self.master.top_frame.var_major_version.get()
        small_version = self.master.top_frame.var_minor_version.get()

        cocos_pro_root = self.master.top_frame.var_cocos_pro_root.get()
        with open(cocos_pro_root + '/assets/src/constant/VersionConstant.ts', 'r', encoding='utf-8') as f:
            ts_file = f.read()

        ts_file = ts_file.replace(f'export let bigVersion: number = {big_version};', 'export let bigVersion: number = null;')
        ts_file = ts_file.replace(f'export let smallVersion: string = "{small_version}";', 'export let smallVersion: string = null;')

        with open(cocos_pro_root + '/assets/src/constant/VersionConstant.ts', 'w', encoding='utf-8') as f:
            f.write(ts_file)
