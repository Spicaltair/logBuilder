import sys
import os
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


# 添加 scripts utils 目录到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from log_creator import create_log_file

# 导入 get_weather_by_location 模块中的函数
from get_weather_by_location import get_weather_by_location

def save_log():
    """
    保存日志内容到文件或数据库
    """
    date = entry_date.get()
    task = entry_task.get("1.0", tk.END).strip()
    weather = entry_weather.get("1.0", tk.END).strip()  # 获取多行文本内容并去除多余的空格

    
    if not date or not task:
        messagebox.showerror("错误", "日期和任务内容不能为空！")
        return
    
    log_content = f"日期: {date}\n任务: {task}\n天气: {weather}\n"
    log_path = create_log_file(directory="logs", logs=log_content)
    
    messagebox.showinfo("成功", f"日志已保存到: {log_path}")
    entry_task.delete("1.0", tk.END)

# 创建主窗口
root = tk.Tk()
root.title("施工日志工具")

# 自动获取当前日期和天气
current_date = datetime.now().strftime("%Y-%m-%d")
current_weather = get_weather_by_location()  # 使用 scripts/get_weather.py 中的函数

# 日期输入
label_date = tk.Label(root, text="日期（自动获取）:")
label_date.pack(pady=5)
entry_date = tk.Entry(root, width=30)
entry_date.insert(0, current_date)  # 自动填入当前日期
entry_date.pack(pady=5)

# 任务输入
label_task = tk.Label(root, text="任务内容:")
label_task.pack(pady=5)
entry_task = tk.Text(root, width=50, height=10)
entry_task.pack(pady=5)

# 天气输入
def format_weather_data(weather_data):
    """
    将字典格式化为字符串以便在 GUI 中显示
    """
    formatted = ""
    for key, value in weather_data.items():
        if isinstance(value, dict):
            # 如果值是嵌套字典，递归格式化
            formatted += f"{key}:\n" + format_weather_data(value) + "\n"
        elif isinstance(value, list):
            # 如果值是列表，格式化列表中的每个元素
            formatted += f"{key}:\n"
            for item in value:
                formatted += f"  - {item}\n"
        else:
            # 普通键值对
            formatted += f"{key}: {value}\n"
    return formatted

# 替换单行 Entry 为多行 Text
label_weather = tk.Label(root, text="天气（自动获取，可修改）:")
label_weather.pack(pady=5)
entry_weather = tk.Text(root, width=50, height=10)  # 使用多行文本框
entry_weather.pack(pady=5)

# 插入格式化后的天气信息
formatted_weather = format_weather_data(current_weather)
entry_weather.insert("1.0", formatted_weather)


# 保存按钮
btn_save = tk.Button(root, text="保存日志", command=save_log)
btn_save.pack(pady=10)

# 启动 GUI
root.mainloop()
