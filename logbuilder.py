import os
import sys


print("Script is running...")
print(sys.path)
try:
    # 确保路径添加正确
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print(f"Current working directory: {os.getcwd()}")
    sys.path.append(os.getcwd())  # 确保当前目录在模块搜索路径中
    print(f"Module search path: {sys.path}")
    print("Checking if 'app/main.py' exists:", os.path.exists("app/main.py"))
    print("Checking if 'app/gui.py' exists:", os.path.exists("app/gui.py"))

    print("Paths appended:", sys.path)

    # 导入模块
    from app.main import run_main_app
    from app.gui import run_gui
    from scripts.init_db import initialize_database


    print("Modules imported successfully.")

    if __name__ == "__main__":
        print("Inside main block...")

        # 核心逻辑
        print("Running main app...")
        run_main_app()

        # 数据库初始化
        print("Initializing database...")
        initialize_database()

        # GUI 启动
        print("Starting GUI...")
        run_gui()
except ImportError as e:
    print(f"ImportError occurred: {e}")
except Exception as e:
    print(f"Other error occurred: {e}")
