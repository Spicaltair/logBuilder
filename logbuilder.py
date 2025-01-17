import os
import sys
import tkinter as tk

# 打印当前工作目录和模块搜索路径
print(f"Current working directory: {os.getcwd()}")
print(f"Module search path: {sys.path}")

try:
    # 创建 Tkinter 主窗口（仅用于测试）
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口，避免阻塞运行

    # 尝试导入模块
    print("Attempting to import modules...")
    from app.main import run_main_app
    from app.gui import run_gui
    from scripts.init_db import init_database

    print("Modules imported successfully.")
except ModuleNotFoundError as e:
    print(f"ModuleNotFoundError occurred: {e}")
except ImportError as e:
    print(f"ImportError occurred: {e}")
except Exception as e:
    print(f"Other error occurred: {e}")
finally:
    if 'root' in locals():
        root.destroy()  # 确保窗口被销毁


    if __name__ == "__main__":
        print("Inside main block...")

        # 核心逻辑
        print("Running main app...")
        run_main_app()

        # 数据库初始化
        print("Initializing database...")
        init_database()

        # GUI 启动
        print("Starting GUI...")
        run_gui()

