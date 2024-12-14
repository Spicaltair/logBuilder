import os
import sys
from utils.log_creator import create_log_file
from utils.history_manager import load_history



def run_main_app():
    """
    主应用核心业务逻辑，
    处理施工日志功能，
    加载用户信息，天气管理
    """
    print("欢迎使用乐标日志 LogBuilder！")
  
    # 调用时，您可以选择性地传递 filename 参数
    log_directory = "logs"
    
    log_content = "这是第一条日志This is the first log entry.\n"
    

    # 调用日志创建功能
    log_path = create_log_file(directory=log_directory,logs=log_content)
    print(f"日志文件已创建: {log_path}")

    # 加载用户历史选择
    last_city = load_history()
    print(f"加载历史城市: {last_city}")

 
    # 后续扩展功能
    print("其他功能开发中...")
