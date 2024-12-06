import os
from datetime import datetime
import sys
from app.main import run_main_app
from app.gui import run_gui

# 添加项目根目录到 Python 搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    print("Initializing LogBuilder...")
    run_main_app()
    print("LogBuilder application has exited.")

