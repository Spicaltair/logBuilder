import os
import sys

print("Script is running...")

try:
    # 确保路径添加正确
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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
except Exception as e:
    print(f"Error occurred: {e}")
