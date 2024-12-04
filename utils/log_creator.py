import os
from datetime import datetime

def create_log_file(directory, logs):
    """
    创建日志文件并写入日志内容。

    参数:
    - directory: 日志存储目录
    - logs: 日志内容，可以是单行字符串或多行日志列表
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"log_{timestamp}.txt"
    filepath = os.path.join(directory, filename)

    with open(filepath, "w", encoding="utf-8") as file:
        file.write("== 项目日志文件 ==\n")
        file.write(f"创建时间: {datetime.now()}\n\n")
        if isinstance(logs, list):
            for log in logs:
                file.write(log + "\n")
        else:
            file.write(logs + "\n")

    return filepath