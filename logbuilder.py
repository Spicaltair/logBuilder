import os
import sys
from app.main import run_main_app
from app.gui import run_gui

# 添加项目根目录到 Python 搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    print("Initializing LogBuilder...")
    print("欢迎使用乐标日志 LogBuilder！")
    
    # 启动核心逻辑（如创建日志文件等）
    run_main_app()

    # 启动 GUI
    run_gui()