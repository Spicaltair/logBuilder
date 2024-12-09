import sys
import os
import tkinter as tk

from tkinter import ttk  # 导入 ttk 模块
from tkinter import messagebox
from datetime import datetime
from tkcalendar import DateEntry  # 导入 DateEntry 控件


# 添加 scripts utils 目录到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from log_creator import create_log_file
from get_location import get_city

from api_utils import get_dynamic_city_list, get_weather, get_location_data



# 函数区》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
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
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", "请输入有效的城市名称！")
        return

    weather = get_weather(city)
    if 'error' in weather:
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", weather['error'])
    else:
        result = (
            f"城市: {city}\n"
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", result)

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
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", weather['error'])
    else:
        result = (
            f"城市: {city}\n"
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", result)


#初始化
def initialize_defaults():
    """
    自动填入默认的城市和天气信息
    """
    # 自动填入城市
    default_city = select_city()
    entry_city.insert(0, default_city)

    # 自动填入天气
    weather = get_weather_by_location()
    if 'error' not in weather:
        result = (
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        entry_weather.insert("1.0", result)
    else:
        entry_weather.insert("1.0", weather['error'])

#函数区《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
    

#窗口布置区》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# 创建主窗口

bg_color = "#CFDEE6"  # 主背景颜色（灰白）
bg_label_color = "#234406" # 主背景颜色（深绿）
bg_button_color = "#007BFF" #按钮背景颜色（天蓝）

bg_color_test = "#CB7A00"  # 主背景颜色（深绿）

fg_color_white="#e6f0ea" # 前景（白色）
fg_color_black="#ffffff" #前景（黑色）

root = tk.Tk()
root.title("LogBuilder！！ ")
root.geometry("400x500")
root.config(bg=bg_color)  # 设置背景颜色-深绿

# 添加一个标签
label = tk.Label(root, text="欢迎使用施工日志工具乐构者", bg=bg_label_color, fg="#e6f0ea", font=("Arial", 16))
label.pack(pady=15)


#窗口布置区《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
#画布和滚动条配置--------------------------------------------------------
# 创建画布和滚动
canvas = tk.Canvas(root, bg=bg_color)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg=bg_color)

# 配置滚动条
scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
#-------------------------------------------------------------------------------

# 自动获取当前日期、城市和天气
# 日期输入
current_date = datetime.now().strftime("%Y-%m-%d")
# 日期区
frame_date = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_date.pack(fill="x")

label_date = tk.Label(frame_date, bg=bg_label_color, fg="#e6f0ea", text="日期（自动获取）:")
label_date.pack(pady=5)

frame_date = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_date.pack(fill="x")

label_date = tk.Label(frame_date, bg=bg_label_color, fg="#e6f0ea", text="选择日期:")
label_date.pack(pady=5)

# 使用 DateEntry 控件
entry_date = DateEntry(frame_date, width=20, date_pattern="yyyy-mm-dd", background='darkblue', foreground='white', borderwidth=2)
entry_date.pack(pady=5)


# 城市区
frame_city = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_city.pack(fill="x")

label_city = tk.Label(frame_city, text="选择或输入城市:", bg=bg_label_color, fg="#e6f0ea")
label_city.pack(pady=5)

# 获取动态城市列表
cities = get_dynamic_city_list()  # 动态城市列表函数

# 创建城市选择和输入框
entry_city = ttk.Combobox(frame_city, values=cities, state="normal", width=30)  # 可输入和选择
entry_city.set(cities[0])  # 默认选择第一个城市
entry_city.pack(pady=10)

# 自动检测城市按钮
btn_update_city = tk.Button(frame_city, text="自动检测城市", bg=bg_button_color, fg=fg_color_black, command=update_city_entry)
btn_update_city.pack(pady=5)

# 获取当前选中或输入的城市
def get_selected_city():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("警告", "请输入或选择一个城市！")
    return city

# 自动检测城市逻辑
def update_city_entry():
    detected_city = "自动检测到的城市"  # 替换为自动检测逻辑
    entry_city.set(detected_city)

# 天气区
frame_weather = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_weather.pack(fill="x")

label_weather = tk.Label(frame_weather, bg=bg_label_color, fg="#e6f0ea", text="天气信息:")
label_weather.pack(pady=5)

entry_weather = tk.Text(frame_weather, width=50, height=10, bg="#ffffff", fg="#000000")
entry_weather.pack()

btn_fetch_weather = tk.Button(frame_weather, text="获取天气", bg=bg_button_color, fg=fg_color_white, command=fetch_weather)
btn_fetch_weather.pack(pady=5)

# 初始化时自动填入城市
update_city_entry()

# 任务区
frame_task = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_task.pack(fill="x")

label_task_title = tk.Label(frame_task, text="任务", bg=bg_label_color, fg=fg_color_white)
label_task_title.pack()

entry_task = tk.Text(frame_task, width=50, height=5, bg="#ffffff", fg=fg_color_black)
entry_task.pack()

# 保存按钮
btn_save = tk.Button(frame_task, bg=bg_button_color, fg=fg_color_white, text="保存日志", command=save_log)
btn_save.pack(side="bottom", padx=5)
# 预览按钮
btn_preview = tk.Button(frame_task, bg=bg_button_color, fg=fg_color_white, text="预览日志", command=preview_log)
btn_preview.pack(side="bottom", padx=5)

# 插入默认文字
entry_task.insert("1.0", "请输入今天的任务")  # "1.0" 表示从第一行第一个字符开始

def clear_default(event):
    if entry_task.get("1.0", tk.END).strip() == "请输入今天的任务":
        entry_task.delete("1.0", tk.END)


entry_task.bind("<FocusIn>", clear_default)  # 绑定焦点事件




# 启动 GUI
root.mainloop()
