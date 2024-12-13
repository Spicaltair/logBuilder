import sys
import os
import tkinter as tk
import sqlite3

from tkinter import ttk  # 导入 ttk 模块
from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
from tkcalendar import DateEntry  # 导入 DateEntry 控件

from collections import Counter



# 添加 scripts utils 目录到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from log_creator import create_log_file
from get_location import get_city

from api_utils import get_dynamic_city_list, get_weather, get_location_data

from translate import Translator


# 函数区》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》

def translate_city_third_party(city_name):
    translator = Translator(to_lang="zh")
    translation = translator.translate(city_name)
    return translation

weekday_mapping = {
    "Monday": "星期一",
    "Tuesday": "星期二",
    "Wednesday": "星期三",
    "Thursday": "星期四",
    "Friday": "星期五",
    "Saturday": "星期六",
    "Sunday": "星期日"
}


def save_log():
    """
    保存日志内容到文件
    """
    date = entry_date.get()
    city = entry_city.get()
    weather = entry_weather.get("1.0", tk.END).strip()

    if not tasks:
        tasks_content = "无任务记录"
    else:
        tasks_content = "\n".join([f"{idx}. {task}" for idx, task in enumerate(tasks, start=1)])
    
    # 拼接日志内容
    log_content = (
        f"日期: {date}\n"
        f"城市: {city}\n"
        f"天气信息:\n{weather}\n\n"
        f"任务列表:\n{tasks_content}\n"
    )

    # 保存到文件
    log_path = create_log_file(directory="logs", logs=log_content)
    messagebox.showinfo("成功", f"日志已保存到: {log_path}")

    # 清空任务输入框
    entry_task.delete("1.0", tk.END)
    tasks.clear()  # 清空任务列表
    refresh_task_display()  # 刷新任务显示框


# 预览函数定义
def preview_log():
    """
    显示日志预览窗口，包含日期、任务列表、天气等内容
    """
    # 获取日志信息
    date = entry_date.get()
    city = entry_city.get()
    weather = entry_weather.get("1.0", tk.END).strip()
    
    if not tasks:
        tasks_preview = "无任务记录"
    else:
        tasks_preview = "\n".join([f"{idx}. {task}" for idx, task in enumerate(tasks, start=1)])

    # 创建新窗口显示内容
    preview_window = tk.Toplevel(root)
    preview_window.title("日志预览")

    preview_content = (
        f"日期: {date}\n"
        f"城市: {city}\n"
        f"天气信息:\n{weather}\n\n"
        f"任务列表:\n{tasks_preview}"
    )
    label_preview = tk.Label(preview_window, text=preview_content, justify="left", anchor="w")
    label_preview.pack(padx=10, pady=10)

    btn_close = tk.Button(preview_window, text="关闭", command=preview_window.destroy)
    btn_close.pack(pady=5)


def save_task_to_db(date, content, status="未完成"):
    """
    将任务保存到数据库
    """
    conn = sqlite3.connect("construction_logs.db")  # 数据库文件路径
    cursor = conn.cursor()

    # 创建 tasks 表（如果不存在）
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            content TEXT NOT NULL,
            status TEXT DEFAULT '未完成'
        );
    ''')

    # 插入任务
    cursor.execute('''
        INSERT INTO tasks (date, content, status)
        VALUES (?, ?, ?)
    ''', (date, content, status))

    conn.commit()
    conn.close()


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
# 鼠标滚轮支持
def _on_mouse_wheel(event):
    canvas.yview_scroll(-1 * (event.delta // 120), "units")

canvas.bind_all("<MouseWheel>", _on_mouse_wheel)
#-------------------------------------------------------------------------------

# 自动获取当前日期、城市和天气
# 获取当前日期和星期
current_date = datetime.now().strftime("%Y-%m-%d")
current_weekday = datetime.now().strftime("%A")  # 获取英文星期几

# 日期区
frame_date = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_date.pack(fill="x")

# 日期标签
label_date = tk.Label(frame_date, text="日期（自动获取）:", bg=bg_label_color, fg="#e6f0ea")
label_date.pack(pady=5)


def update_weekday(*args):
    """
    更新星期几显示
    """
    selected_date = entry_date.get_date()  # 获取选定的日期
    weekday = selected_date.strftime("%A")
    label_weekday.config(text=f"星期: {weekday}")

entry_date = DateEntry(frame_date, width=20, background='darkblue', foreground='white', borderwidth=2)
entry_date.pack(pady=5)
entry_date.bind("<<DateEntrySelected>>", update_weekday)

# 星期显示标签
label_weekday = tk.Label(frame_date, text=f"星期: {current_weekday}", bg=bg_label_color, fg="#e6f0ea")
label_weekday.pack(pady=5)


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

# 新增：标签用于显示翻译后的中文城市
label_city_translated = tk.Label(frame_city, text="", bg=bg_label_color, fg="#e6f0ea")
label_city_translated.pack(pady=5)

# 自动检测城市按钮
btn_update_city = tk.Button(frame_city, text="自动检测城市", bg=bg_button_color, fg=fg_color_black, command=lambda: update_city_entry(label_city_translated))
btn_update_city.pack(pady=5)

# 获取当前选中或输入的城市
def get_selected_city():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("警告", "请输入或选择一个城市！")
        return None
    return city

# 自动检测城市逻辑（只修改显示的翻译，不修改 entry_city 的值）
def update_city_entry(label_translated):
    detected_city = "自动检测到的城市"  # 替换为自动检测逻辑
    translated_city = translate_city_third_party(detected_city)
    label_translated.config(text=f"中文城市: {translated_city}")

# 天气区
frame_weather = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_weather.pack(fill="x")

label_weather = tk.Label(frame_weather, bg=bg_label_color, fg="#e6f0ea", text="天气信息:")
label_weather.pack(pady=5)

entry_weather = tk.Text(frame_weather, width=50, height=10, bg="#ffffff", fg="#000000")
entry_weather.pack()

btn_fetch_weather = tk.Button(frame_weather, text="获取天气", bg=bg_button_color, fg=fg_color_white, command=fetch_weather)
btn_fetch_weather.pack(pady=5)



# 任务区
task_history = Counter()  # 用于存储任务及其出现次数
tasks = [] #定义任务列表
frame_task = tk.Frame(scrollable_frame, bg=bg_color, pady=10)
frame_task.pack(fill="x")

# 任务显示框
label_task_list = tk.Label(frame_task, text="任务列表:", bg=bg_label_color, fg="#e6f0ea")
label_task_list.pack(pady=5)

task_display = tk.Text(frame_task, width=50, height=10, state="normal", wrap="word")
task_display.pack(pady=5)
# 任务建议标签
label_suggestions = tk.Label(frame_task, text="历史任务建议:", bg=bg_label_color, fg="#e6f0ea")
label_suggestions.pack(pady=5)

def select_task_from_history(event):
    """
    用户从任务建议中选择任务后填充到输入框
    """
    selected_task = combobox_task.get().strip()
    entry_task.delete("1.0", tk.END)
    entry_task.insert("1.0", selected_task)

# 创建任务建议下拉菜单
combobox_task = ttk.Combobox(frame_task, width=50, state="readonly")
combobox_task.pack(pady=5)
combobox_task.bind("<<ComboboxSelected>>", select_task_from_history)

# 任务输入框
label_task = tk.Label(frame_task, text="任务内容:", bg=bg_label_color, fg="#e6f0ea")
label_task.pack(pady=5)

# 任务输入框
entry_task = tk.Text(frame_task, width=50, height=10)
entry_task.pack(pady=5)


def add_task():
    """
    添加任务到任务列表，并更新历史记录
    """
    task = entry_task.get("1.0", tk.END).strip()
    date = entry_date.get()  # 从日期输入框获取值
    
    if not task:
        messagebox.showwarning("警告", "任务内容不能为空！")
        return

    tasks.append(task) # 添加到内存列表
    task_history[task] += 1
    save_task_to_db(date, task)  # 保存到数据库
    refresh_task_display()  # 刷新任务显示
    refresh_task_suggestions()  # 刷新任务建议
    entry_task.delete("1.0", tk.END)  # 清空输入框


def refresh_task_suggestions():
    """
    刷新任务建议下拉菜单，显示高频任务
    """
    sorted_tasks = [task for task, _ in task_history.most_common(10)]
    combobox_task['values'] = sorted_tasks






def delete_task():
    """
    删除光标所在行的任务
    """
    try:
        # 获取光标所在的行号
        cursor_index = task_display.index(tk.INSERT)  # 获取光标位置
        line_number = int(cursor_index.split(".")[0])  # 提取行号

        # 检查是否存在任务
        if line_number > len(tasks):
            messagebox.showwarning("警告", "光标未定位在任务行内！")
            return

        # 删除任务
        tasks.pop(line_number - 1)  # 删除列表中的任务
        refresh_task_display()  # 更新任务显示
    except Exception as e:
        messagebox.showerror("错误", f"删除任务失败: {e}")


def clear_tasks():
    """
    清空所有任务
    """
    if messagebox.askyesno("确认", "确定清空所有任务吗？"):
        tasks.clear()  # 清空任务列表
        refresh_task_display()  # 更新任务显示


def mark_task_completed():
    """
    标记光标所在行的任务为完成
    """
    try:
        # 获取光标所在的行号
        cursor_index = task_display.index(tk.INSERT)  # 获取光标位置
        line_number = int(cursor_index.split(".")[0])  # 提取行号

        # 检查是否存在任务
        if line_number > len(tasks):
            messagebox.showwarning("警告", "光标未定位在任务行内！")
            return

        # 标记任务完成
        tasks[line_number - 1] += " ✅"
        refresh_task_display()  # 更新任务显示
    except Exception as e:
        messagebox.showerror("错误", f"标记任务失败: {e}")


def refresh_task_display():
    """
    刷新任务显示框中的内容，显示任务编号
    """
    task_display.delete("1.0", tk.END)  # 清空任务显示框
    for idx, task in enumerate(tasks, start=1):  # 为任务添加编号
        task_display.insert(tk.END, f"{idx}. {task}\n")  # 显示任务带编号

def refresh_task_suggestions():
    """
    刷新任务建议下拉菜单，显示高频任务
    """
    sorted_tasks = [task for task, _ in task_history.most_common(10)]  # 取前10个高频任务
    combobox_task['values'] = sorted_tasks  # 更新下拉菜单的值

def select_task_from_history(event):
    """
    用户从任务建议中选择任务后填充到输入框
    """
    selected_task = combobox_task.get().strip()
    entry_task.delete("1.0", tk.END)
    entry_task.insert("1.0", selected_task)
        
# 添加任务按钮
btn_add_task = tk.Button(frame_task, text="添加任务", bg=bg_button_color, fg=fg_color_white, command=add_task)
btn_add_task.pack(side="left", padx=5, pady=5)

# 删除任务按钮
btn_delete_task = tk.Button(frame_task, text="删除任务", bg=bg_button_color, fg=fg_color_white, command=delete_task)
btn_delete_task.pack(side="left", padx=5, pady=5)

# 清空任务按钮
btn_clear_tasks = tk.Button(frame_task, text="清空任务", bg=bg_button_color, fg=fg_color_white, command=clear_tasks)
btn_clear_tasks.pack(side="left", padx=5, pady=5)

# 标记完成按钮（可选）
btn_mark_completed = tk.Button(frame_task, text="标记完成", bg=bg_button_color, fg=fg_color_white, command=mark_task_completed)
btn_mark_completed.pack(side="left", padx=5, pady=5)

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
