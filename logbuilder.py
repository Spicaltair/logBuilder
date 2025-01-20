import os
import sys
import tkinter as tk
sys.path.append(os.path.join(os.getcwd(), "data"))
# 打印当前工作目录和模块搜索路径
print(f"Current working directory: {os.getcwd()}")
print(f"Module search path: {sys.path}")

# 确保项目根目录在 sys.path 中
project_root = os.path.dirname(os.path.abspath(__file__))


if project_root not in sys.path:
    sys.path.append(project_root)

root = None
try:
    # 创建 Tkinter 主窗口（仅用于测试）
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口，避免阻塞运行

    # 尝试导入模块
    print("Attempting to import modules...")
    print(f"Current sys.path: {sys.path}")

    from app.main import run_main_app
    from app.gui import run_gui
    

    try:
        # 尝试导入 init_database
        from data.init_db import init_database
        print("init_database function imported successfully.")
    except Exception as e:
        print(f"Error importing init_database: {e}")
except ModuleNotFoundError as e:
    print(f"ModuleNotFoundError occurred: {e}")
except ImportError as e:
    print(f"ImportError occurred: {e}")
except Exception as e:
    print(f"Other error occurred: {e}")
finally:
    if 'root' in locals():
        root.destroy()  # 确保窗口被销毁

# 程序启动时创建 Tkinter 根窗口
def create_root():
    root = tk.Tk()
    root.withdraw()  # 隐藏窗口，避免阻塞运行
    return root
# 主程序逻辑
if __name__ == "__main__":
    print("Inside main block...")
    root = create_root()  # 在主程序块中创建 root
    try:
        # 核心逻辑
        print("Running main app...")
        run_main_app()
    except Exception as e:
        print(f"Error while running main app: {e}")

    try:
        # GUI 启动
        print("Starting GUI...")
        run_gui()
    except Exception as e:
        print(f"Error while starting GUI: {e}")

    try:
        # 数据库初始化
        print("Initializing database...")
        init_database()
    except Exception as e:
        print(f"Error while initializing database: {e}")
