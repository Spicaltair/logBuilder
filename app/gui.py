import sys
import os
import requests
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from ttkthemes import ThemedTk


# 添加 scripts utils 目录到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from log_creator import create_log_file
from get_location import get_city



def save_log():
    """
    保存日志内容到文件或数据库
    """
    date = entry_date.get()
    city = entry_city.get()
    task = entry_task.get("1.0", tk.END).strip()
    weather = entry_weather.get("1.0", tk.END).strip()  # 获取多行文本内容并去除多余的空格

    
    if not date or not task:
        messagebox.showerror("错误", "日期和任务内容不能为空！")
        return
    
    log_content = f"日期: {date}\n城市：{city}\n任务: {task}\n天气: {weather}\n"
    log_path = create_log_file(directory="logs", logs=log_content)
    
    messagebox.showinfo("成功", f"日志已保存到: {log_path}")
    entry_task.delete("1.0", tk.END)

# 预览函数定义
def preview_log():
    """
    显示日志预览窗口
    """
    date = entry_date.get()
    city = entry_city.get()
    task = entry_task.get("1.0", tk.END).strip()
    weather = entry_weather.get("1.0", tk.END).strip()

    # 创建新窗口显示内容
    preview_window = tk.Toplevel(root)
    preview_window.title("日志预览")

    preview_content = f"日期: {date}\n城市：{city}\n任务: {task}\n天气: {weather}"
    label_preview = tk.Label(preview_window, text=preview_content, justify="left")
    label_preview.pack(padx=10, pady=10)

    btn_close = tk.Button(preview_window, text="关闭", command=preview_window.destroy)
    btn_close.pack(pady=5)

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



def update_weather_display():
    """
    根据用户输入的城市更新天气信息
    """
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("警告", "请输入城市名称！")
        return

    weather = get_weather(city)  # 获取天气
    if 'error' in weather:
        weather_output.delete("1.0", tk.END)
        weather_output.insert("1.0", weather['error'])
    else:
        result = (
            f"城市: {city}\n"
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        weather_output.delete("1.0", tk.END)
        weather_output.insert("1.0", result)

    
# 创建主窗口
root = tk.Tk()
root.title("LogBuilder！！ ")
root.geometry("400x500")
root.config(bg="#e6f0ea")  # 设置背景颜色-深绿

#root = ThemedTk(theme="equilux")
# 添加一个标签
label = tk.Label(root, text="欢迎使用施工日志工具乐构者", bg="#27362d", fg="#e6f0ea", font=("Arial", 14))
label.pack(pady=15)

# 创建画布和滚动
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

# 配置滚动条
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# 自动获取当前日期、城市和天气
def select_city():
    """
    自动选择当前城市
    """
    location_data = get_location_data()
    if 'error' in location_data:
        return "未知城市"
    return get_city(location_data)
    
    
def get_weather_by_location():
    """
    根据当前 IP 获取位置并获取天气
    """
    location_data = get_location_data()
    city = get_city(location_data)
    return get_weather(city)
    
def get_location_data():
    """
    获取地理信息并返回字典
    """
    response = requests.get('https://ipinfo.io/json')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error {response.status_code}: {response.reason}"}

def get_city(location_data):
    """
    从地理信息中提取城市
    """
    return location_data.get('city', '未知城市')

def get_weather(city):
    """
    根据城市名称获取天气信息
    """
    api_key = "a50b80b50d70a0d26b0f43b6e2f03e4b"  # 替换为实际 API 密钥
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return {
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }
    else:
        return {'error': f"Error {response.status_code}: {response.reason}'"}

def update_city_entry():
    """
    自动填入当前检测到的城市
    """
    location_data = get_location_data()
    if 'error' in location_data:
        default_city = "未知城市"
    else:
        default_city = get_city(location_data)

    entry_city.delete(0, tk.END)
    entry_city.insert(0, default_city)

def fetch_weather():
    """
    获取天气信息并显示
    """
    city = entry_city.get().strip()
    if not city:
        weather_output.delete("1.0", tk.END)
        weather_output.insert("1.0", "请输入有效的城市名称！")
        return

    weather = get_weather(city)
    if 'error' in weather:
        weather_output.delete("1.0", tk.END)
        weather_output.insert("1.0", weather['error'])
    else:
        result = (
            f"城市: {city}\n"
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        weather_output.delete("1.0", tk.END)
        weather_output.insert("1.0", result)
current_date = datetime.now().strftime("%Y-%m-%d")
current_city = select_city()
current_weather = get_weather_by_location()  # 使用 scripts/get_weather.py 中的函数

# 日期输入
label_date = tk.Label(scrollable_frame, bg="#27362d", fg="#e6f0ea", text="日期（自动获取）:")
label_date.pack(pady=5)
entry_date = tk.Entry(scrollable_frame,  width=30)
entry_date.insert(0, current_date)  # 自动填入当前日期
entry_date.pack(pady=5)






# 创建 GUI 主窗口

root.title("天气获取工具")
root.geometry("400x300")
root.config(bg="#27362d")

# 城市输入部分
label_city = tk.Label(root, bg="#27362d", fg="#e6f0ea", text="输入城市:")
label_city.pack(pady=5)
entry_city = tk.Entry(root, width=30)
entry_city.pack(pady=5)

btn_update_city = tk.Button(root, text="自动检测城市", bg="#007BFF", fg="#ffffff", command=update_city_entry)
btn_update_city.pack(pady=5)

# 天气显示部分
btn_fetch_weather = tk.Button(root, text="获取天气", bg="#007BFF", fg="#ffffff", command=fetch_weather)
btn_fetch_weather.pack(pady=5)

weather_output = tk.Text(root, width=40, height=10, wrap="word", bg="#ffffff", fg="#000000")
weather_output.pack(pady=5)

# 初始化时自动填入城市
update_city_entry()

# 任务输入
label_task = tk.Label(scrollable_frame, bg="#27362d", fg="#e6f0ea", text="任务内容:")
label_task.pack(pady=5)

entry_task = tk.Text(scrollable_frame, width=50, height=10)  # 创建 Text 小部件
entry_task.pack(pady=5)

# 插入默认文字
entry_task.insert("1.0", "请输入今天的任务")  # "1.0" 表示从第一行第一个字符开始

def clear_default(event):
    if entry_task.get("1.0", tk.END).strip() == "请输入今天的任务":
        entry_task.delete("1.0", tk.END)

entry_task.bind("<FocusIn>", clear_default)  # 绑定焦点事件

# 按钮区------------------------------------------------------------------------------------
# 保存按钮
btn_save = tk.Button(scrollable_frame, bg="#27362d", fg="#e6f0ea", text="保存日志", command=save_log)
btn_save.pack(side="left", padx=5)
# 预览按钮
btn_preview = tk.Button(scrollable_frame, bg="#27362d", fg="#e6f0ea", text="预览日志", command=preview_log)
btn_preview.pack(side="left", padx=5)
# 获取天气按钮
btn_get_weather = tk.Button(scrollable_frame,bg="#27362d", fg="#e6f0ea", text="获取天气", command=update_weather_display)
btn_get_weather.pack(side="left", padx=5)  # 增加内边距和垂直间距

#-------------------------------------------------------------
# 启动 GUI
root.mainloop()
