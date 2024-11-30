import os
from datetime import datetime
import sys
import os

# 添加项目根目录到 Python 搜索路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def create_log_file(directory="logs", filename=None, content=None):
    """
    创建一个日志文件。

    Args:
        directory (str): 存放日志的目录，默认是 'logs'。
        filename (str): 日志文件名，默认为当前时间戳。
        content (str): 初始日志内容，默认是空字符串。

    Returns:
        str: 创建的日志文件路径。
    """
    # 设置默认文件名
    if filename is None:
        filename = f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # 确保目录存在
    os.makedirs(directory, exist_ok=True)

    # 创建文件路径
    filepath = os.path.join(directory, filename)

    # 写入内容
    with open(filepath, "w") as file:
        file.write(content or "Log Initialized.\n")

    print(f"施工日志文件创建在: {filepath}")
    return filepath

from utils.log_creator import create_log_file

if __name__ == "__main__":
    # 示例：创建一个日志文件
    log_path = create_log_file("logs", "This is the first log entry.\n")
    
