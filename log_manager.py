# log_manager.py

import sqlite3
from tkinter import messagebox
from utils.api_utils import get_weather
from datetime import datetime

db_path = "data/construction_logs.db"  # 固定数据库路径

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

def preview_log(date, city, weather, tasks):
    """
    显示日志预览窗口，包含日期、任务列表、天气、项目名称和日志记录者信息。
    """
    if not tasks:
        tasks_preview = "无任务记录"
    else:
        tasks_preview = "\n".join([f"{idx}. {task}" for idx, task in enumerate(tasks, start=1)])

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
                SELECT project_name, user_name 
                FROM Users_Projects 
                WHERE date = ? 
                ORDER BY id DESC 
                LIMIT 1 
            ''', (date,))
            result = cursor.fetchone()
            if result:
                project_name, user_name = result
            else:
                project_name, user_name = "未知项目", "未知用户"
    except sqlite3.DatabaseError as e:
        messagebox.showerror("数据库错误", f"无法获取项目信息: {e}")
        project_name, user_name = "未知项目", "未知用户"

    # 返回预览信息
    return f"日期: {date}\n城市: {city}\n天气: {weather}\n任务: {tasks_preview}\n项目: {project_name}\n记录者: {user_name}"

def save_log(date, city, weather, tasks, project_name="默认项目", user_name="记录者"):
    """
    保存日志内容到数据库
    """
    if not tasks:
        tasks_content = "无任务记录"
    else:
        tasks_content = "\n".join([f"{idx}. {task}" for idx, task in enumerate(tasks, start=1)])
    
    log_content = (
        f"日期: {date}\n"
        f"城市: {city}\n"
        f"天气信息:\n{weather}\n\n"
        f"任务列表:\n{tasks_content}\n"
        f"项目名称: {project_name}\n"
        f"记录者: {user_name}\n"
    )

    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Logs (date, city, weather, tasks, project_name, user_name)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (date, city, weather, tasks_content, project_name, user_name))
            conn.commit()
            messagebox.showinfo("成功", f"日志已保存到数据库。")
    except sqlite3.DatabaseError as e:
        messagebox.showerror("数据库错误", f"保存日志失败: {e}")

def fetch_weather_data(city):
    """
    获取天气信息
    """
    weather = get_weather(city)
    if 'error' in weather:
        return weather['error']
    else:
        result = (
            f"城市: {city}\n"
            f"天气: {weather['description']}\n"
            f"温度: {weather['temperature']}°C\n"
            f"湿度: {weather['humidity']}%\n"
            f"风速: {weather['wind_speed']} m/s\n"
        )
        return result

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
def save_task_to_db(date, content, status="未完成"):
    """
    保存任务到数据库。
    """
    try:
        with sqlite3.connect("construction_logs.db") as conn:
            cursor = conn.cursor()
            # 保存任务到 tasks 表
            cursor.execute('''
                INSERT INTO tasks (date, content, status)
                VALUES (?, ?, ?)
            ''', (date, content, status))
            # 保存到 user_projects 表
            cursor.execute('''
                INSERT INTO user_projects (date, project_name, user_name)
                VALUES (?, ?, ?)
            ''', (date, content, status))
            conn.commit()
    except sqlite3.DatabaseError as e:
        messagebox.showerror("数据库错误", f"数据库操作失败: {e}")


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
    save_task_to_db(date, task,status="未完成")  # 保存到数据库
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

# 从数据库加载高频任务
def load_high_frequency_tasks():
    try:
        # 连接到数据库
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()

        # 执行查询
        cursor.execute('''
            SELECT content FROM TasksHistory
            ORDER BY frequency DESC, created_at ASC
            LIMIT 10
        ''')

        # 获取任务列表
        tasks = [row[0] for row in cursor.fetchall()]
        
        # 关闭连接
        conn.close()

        return tasks
    except sqlite3.Error as e:
        print("数据库操作失败：", e)
        return []
    

def select_task_from_history(event):
    """
    用户从任务建议中选择任务后填充到输入框
    """
    selected_task = combobox_task.get().strip()
    if selected_task:  # 验证非空内容
        entry_task.delete("1.0", tk.END)
        entry_task.insert("1.0", selected_task)
        update_task_history(selected_task)  # 更新任务历史




def update_task_history(task):
    try:
        # 连接到数据库
        conn = sqlite3.connect('construction_logs.db')
        cursor = conn.cursor()

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
        
        conn.commit()  # 提交事务
        conn.close()  # 关闭连接
    except sqlite3.Error as e:
        print("数据库操作失败：", e)

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


