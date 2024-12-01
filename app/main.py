import os
import sys
from utils.log_creator import create_log_file

def run_main_app():
    """
    主应用逻辑，处理施工日志功能。
    """
    print("欢迎使用乐标日志 LogBuilder！")
   # print(create_log_file)

    # 调用时，您可以选择性地传递 filename 参数
    log_directory = "logs"
    #log_filename = "log1"  # 可以传递自定义文件名
    log_content = "这是第一条日志This is the first log entry.\n"
    

    # 调用日志创建功能
    log_path = create_log_file(directory=log_directory,logs=log_content)
    print(f"日志文件已创建: {log_path}")

    # 后续扩展功能
    print("其他功能开发中...")
