import sys
import os
import tkinter as tk
import sqlite3

from tkinter import messagebox
from tkinter import filedialog
from datetime import datetime
from tkcalendar import DateEntry  # 导入 DateEntry 控件
from tkinter import ttk  #导入ttk，控制标签页

from collections import Counter

# 添加 scripts utils 目录到模块搜索路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'utils')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from utils.log_creator import create_log_file
from scripts.get_location import get_city

from utils.api_utils import get_dynamic_city_list, get_weather, get_location_data

from data.config import font_title_14, font_common_12, bg_button_color, bg_color, bg_label_color, fg_color_black, fg_color_white


# 函数区》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》


def convert_to_chinese_weekday(english_weekday):

    week_map = {

        "Monday": "星期一",

        "Tuesday": "星期二",

        "Wednesday": "星期三",

        "Thursday": "星期四",

        "Friday": "星期五",

        "Saturday": "星期六",

        "Sunday": "星期日"

    }

    return week_map.get(english_weekday, "未知")

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


    # 插入任务
    cursor.execute('''
        INSERT INTO tasks (date, content, status)
        VALUES (?, ?, ?)
    ''', (date, content, status))

    conn.commit()
    conn.close()



def save_task_to_db(date, content, status="未完成"):
    try:
        with sqlite3.connect("construction_logs.db") as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO tasks (date, content, status)
                VALUES (?, ?, ?)
            ''', (date, content, status))
            conn.commit()
    except sqlite3.DatabaseError as e:
        messagebox.showerror("数据库错误", f"数据库操作失败: {e}")


#函数区《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
    


#窗口布置区》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》》
# 创建主窗口
root = tk.Tk()
root.title("LogBuilder！！ ")
root.geometry("800x600")
root.config(bg=bg_color)  # 设置背景颜色-深绿

# 添加一个标签
label = tk.Label(root, text="欢迎使用施工日志工具乐构者", bg=bg_label_color, fg=fg_color_white, font=("Arial", 16))
label.pack(pady=15)


#保存和预览按钮
frame_buttons = tk.Frame(root, bg=bg_color)  # 创建一个新的 Frame 来容纳按钮
frame_buttons.pack(side="right", padx=5, pady=5, anchor="ne")  # 放置在右上角

btn_preview_log = tk.Button(frame_buttons, text="日志预览", bg=bg_button_color, fg=fg_color_white, command=preview_log)
btn_preview_log.pack(side="top", padx=5, pady=5)

btn_save_log = tk.Button(frame_buttons, text="日志保存", bg=bg_button_color, fg=fg_color_white, command=save_log)
btn_save_log.pack(side="top", padx=5, pady=5)
#窗口布置区《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《《
#画布和滚动条配置--------------------------------------------------------
# 创建画布和滚动

# 创建 Notebook（标签页控件）
notebook = ttk.Notebook(root)


# 创建各个标签页的 Frame
frame_date = tk.Frame(notebook, bg=bg_color, pady=15)  # 日期管理
frame_city_weather = tk.Frame(notebook, bg=bg_color, pady=15)  # 城市天气
frame_tasks = tk.Frame(notebook, bg=bg_color, pady=15)  # 任务管理
frame_project = tk.Frame(notebook, bg=bg_color, pady=15)  # 项目管理
frame_user = tk.Frame(notebook, bg=bg_color, pady=15)  # 用户管理

# 将 Frame 添加到 Notebook
notebook.add(frame_date, text="日期管理")
notebook.add(frame_city_weather, text="城市天气")
notebook.add(frame_tasks, text="任务管理")
notebook.add(frame_project, text="项目管理")
notebook.add(frame_user, text="用户管理")
# 在主窗口中显示 Notebook
notebook.pack(fill="both", expand=True)
#-------------------------------------------------------------------------------
# 日期功能区
tk.Label(frame_date, text="日期功能区", bg="#CFDEE6", font=("Arial", 14)).pack(pady=10)

# 日期标签
label_date = tk.Label(frame_date, text="日期（自动获取）:", bg=bg_label_color, fg=fg_color_white)
label_date.pack(pady=5)

# 日期选择器
entry_date = DateEntry(frame_date, width=20, background='darkblue', foreground='white', borderwidth=2)
entry_date.pack(pady=5)

# 更新星期函数
def update_weekday(*args):
    selected_date = entry_date.get_date()  # 获取选定的日期
    current_weekday = selected_date.strftime("%A")
    label_weekday.config(text=f"{selected_date} {convert_to_chinese_weekday(current_weekday)}")

# 绑定更新事件
entry_date.bind("<<DateEntrySelected>>", update_weekday)

# 星期显示标签
# 获取当前选定的日期并显示日期和中文星期
selected_date = entry_date.get_date()
selected_weekday = convert_to_chinese_weekday(selected_date.strftime("%A"))

label_weekday = tk.Label(
    frame_date,
    text=f"{selected_date} {selected_weekday}",
    bg=bg_label_color,
    fg=fg_color_white
)
label_weekday.pack(pady=5)



# 城市功能
tk.Label(frame_city_weather, text="城市和天气功能区", bg=bg_color, font=font_title_14).grid(row=0, column=0, columnspan=2, pady=10)

# 城市区

cities = get_dynamic_city_list()  # 调用函数获取城市列表

label_city = tk.Label(frame_city_weather, text="选择或输入城市:", bg=bg_label_color, fg=fg_color_white)
label_city.grid(row=1, column=0, sticky="e", padx=5, pady=5)  # 对齐到右边

entry_city = ttk.Combobox(frame_city_weather, values=cities, state="normal", width=30)  # 可输入和选择
entry_city.set(cities[0])  # 默认选择第一个城市
entry_city.grid(row=1, column=1, sticky="w", padx=5, pady=5)  # 对齐到左边
print(cities[0])

# 自动检测城市按钮
btn_update_city = tk.Button(frame_city_weather, text="自动检测城市", bg=bg_button_color, fg=fg_color_white, command=lambda: update_city_entry())
btn_update_city.grid(row=3, column=0, columnspan=2, pady=5)  # 跨两列

# 天气区
frame_weather = tk.Frame(frame_city_weather, bg=bg_color, pady=10)
frame_weather.grid(row=0, column=0, sticky="nsew")


label_weather = tk.Label(frame_city_weather, bg=bg_label_color, fg="#e6f0ea", text="天气信息:")
label_weather.grid(row=4, column=0, sticky="e", padx=5, pady=5)

entry_weather = tk.Text(frame_city_weather, width=50, height=5, bg="#ffffff", fg="#000000", wrap="word")
entry_weather.grid(row=4, column=1, sticky="w", padx=5, pady=5)

# 获取当前选中或输入的城市
def get_selected_city():
    city = entry_city.get().strip()
    if not city:
        messagebox.showwarning("警告", "请输入或选择一个城市！")
        return None
    return city    

# 天气输入    
    
def fetch_weather():
    """
    获取天气信息并显示
    """
    city = entry_city.get().strip()
    print(f"City selected: {city}")  # 打印城市名，调试时查看
    if not city:
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", "请输入有效的城市名称！")
        return
    # 如果存在重复城市名，取第一个
    city = city.split()[0]
    print(f"Final city: {city}")  # 再次打印最终的城市名
    weather = get_weather(city)
    if 'error' in weather:
        entry_weather.delete("1.0", tk.END)
        entry_weather.insert("1.0", weather['error'])
        return weather
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
    try:
        # 自动填入城市
        default_city = get_selected_city()
        entry_city.set(default_city)

         # 自动填入天气
        weather = fetch_weather()
        if weather is None or 'error' not in weather:
            print(f"初始化时天气信息出错: {weather.get('error', '未知错误')}")
        else:
            print(f"初始化天气信息成功: {weather}")
    except Exception as e:
        print(f"初始化时发生错误: {e}")
initialize_defaults()

#城市输入

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




btn_fetch_weather = tk.Button(frame_city_weather, text="获取天气", bg=bg_button_color, fg=fg_color_white, command=fetch_weather)
btn_fetch_weather.grid(row=5, column=0, columnspan=2, pady=5)  # 跨两列


# 任务功能
tk.Label(frame_tasks, text="任务功能区", bg=bg_color, fg=fg_color_black, font=font_title_14).pack(pady=10)
# 你可以把任务管理相关的代码放在这里
# 任务区
# 任务建议标签
# 任务区主框架（容器框架，分为左右两部分）
# 任务输入框标题
tasks =[]


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
    save_task_to_db(date, task)  # 保存到数据库
    refresh_task_display()  # 刷新任务显示
    update_task_history(task)  # 更新任务历史
    entry_task.delete("1.0", tk.END)  # 清空输入框


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



def clear_default(event):
    if entry_task.get("1.0", tk.END).strip() == "请输入今天的任务":
        entry_task.delete("1.0", tk.END)


frame_tasks = tk.Frame(frame_tasks, bg=bg_color, pady=10)
frame_tasks.pack(fill="x")

# 左侧：任务显示区
frame_task_list = tk.Frame(frame_tasks, bg=bg_color, width=200, pady=10)
frame_task_list.pack(side="left", fill="y", padx=10)

# 任务显示框标题
label_task_list = tk.Label(frame_task_list, text="任务列表显示:", bg=bg_label_color, fg="#e6f0ea")
label_task_list.pack(side="top", pady=5)

# 任务显示框
task_display = tk.Text(frame_task_list, width=40, height=20, state="normal", wrap="word")
task_display.pack(side="top", pady=5)


# 右侧：任务输入区
frame_task_input = tk.Frame(frame_tasks, bg=bg_color, width=200, pady=10)
frame_task_input.pack(side="right", fill="y", padx=10)

# 历史任务建议标题
label_suggestions = tk.Label(frame_task_input, text="历史任务建议:", bg=bg_label_color, fg="#e6f0ea")
label_suggestions.pack(pady=5)

# 创建任务建议下拉菜单
combobox_task = ttk.Combobox(frame_task_input, width=40, state="readonly")
combobox_task.pack(pady=5)

label_task = tk.Label(frame_task_input, text="任务内容输入框:", bg=bg_label_color, fg="#e6f0ea")
label_task.pack(pady=5)

# 任务输入框
entry_task = tk.Text(frame_task_input, width=40, height=10)
entry_task.pack(pady=5)

# 插入默认文字
entry_task.insert("1.0", "请输入今天的任务")  # 默认提示文字
# 输入区按钮：添加、删除、清空、标记完成
btn_add_task = tk.Button(frame_task_input, text="添加任务", bg=bg_button_color, fg=fg_color_white, command=add_task)
btn_add_task.pack(side="left", padx=5, pady=5)

btn_delete_task = tk.Button(frame_task_input, text="删除任务", bg=bg_button_color, fg=fg_color_white, command=delete_task)
btn_delete_task.pack(side="left", padx=5, pady=5)

btn_clear_tasks = tk.Button(frame_task_input, text="清空任务", bg=bg_button_color, fg=fg_color_white, command=clear_tasks)
btn_clear_tasks.pack(side="right", padx=5, pady=5)

btn_mark_completed = tk.Button(frame_task_input, text="标记完成", bg=bg_button_color, fg=fg_color_white, command=mark_task_completed)
btn_mark_completed.pack(side="right", padx=5, pady=5)

# 数据库初始化
conn = sqlite3.connect("tasks.db")
cursor = conn.cursor()
# 创建任务历史表（如果不存在）
cursor.execute('''
    CREATE TABLE IF NOT EXISTS TasksHistory (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL UNIQUE,
        frequency INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()
# 从数据库加载高频任务
def load_high_frequency_tasks():
    cursor.execute('''
        SELECT content FROM TasksHistory
        ORDER BY frequency DESC, created_at ASC
        LIMIT 10
    ''')
    return [row[0] for row in cursor.fetchall()]
# 从数据库加载任务列表并设置到 Combobox
def update_task_suggestions():
    """
    从数据库加载高频任务，并将其设置到下拉菜单
    """
    task_list = load_high_frequency_tasks()  # 从数据库获取任务列表
    combobox_task["values"] = task_list     # 更新下拉菜单选项
    if task_list:
        combobox_task.current(0)  # 默认选择第一个任务

# 将函数用于初始化和任务添加后刷新建议列表
update_task_suggestions()



def select_task_from_history(event):
    """
    用户从任务建议中选择任务后填充到输入框
    """
    selected_task = combobox_task.get().strip()
    if selected_task:  # 验证非空内容
        entry_task.delete("1.0", tk.END)
        entry_task.insert("1.0", selected_task)
        update_task_history(selected_task)  # 更新任务历史

combobox_task.bind("<<ComboboxSelected>>", select_task_from_history)

# 更新任务频率或插入新任务
def update_task_history(task):
    try:
        # 如果任务存在，更新频率
        cursor.execute('''
            UPDATE TasksHistory
            SET frequency = frequency + 1
            WHERE content = ?
        ''', (task,))
        if cursor.rowcount == 0:
            # 如果任务不存在，插入新任务
            cursor.execute('''
                INSERT INTO TasksHistory (content, frequency)
                VALUES (?, 1)
            ''', (task,))
        conn.commit()
    except sqlite3.Error as e:
        print("数据库操作失败：", e)

def clear_default(event):
    """
    清空默认提示文字
    """
    if entry_task.get("1.0", tk.END).strip() == "请输入今天的任务":
        entry_task.delete("1.0", tk.END)

entry_task.bind("<FocusIn>", clear_default)  # 绑定焦点事件





# 项目管理功能
tk.Label(frame_project, text="项目管理功能区,建设中......", bg="#F4E6E8", font=("Arial", 14)).pack(pady=10)

# 用户管理功能
tk.Label(frame_user, text="用户管理功能区,建设中......", bg="#F4E6E8", font=("Arial", 14)).pack(pady=10)

# 退出前询问是否保存日志
def on_exit():
    # 弹出确认框
    result = messagebox.askyesnocancel("保存日志", "是否保存日志？")
    
    if result is None:  # 取消退出
        return
    elif result:  # 用户选择“是”
        save_log()  # 保存日志
    root.quit()  # 退出程序
# 设置退出时触发的事件
root.protocol("WM_DELETE_WINDOW", on_exit)


# 启动 GUI
root.mainloop()
