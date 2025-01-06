import os
import sqlite3

# 获取当前脚本所在目录的父级目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 指定数据库文件的存储路径
db_path = os.path.join(base_dir, 'data', 'construction_logs.db')

# 确保 data 目录存在
os.makedirs(os.path.dirname(db_path), exist_ok=True)

def initialize_database():
    """
    初始化 SQLite 数据库，创建必要的表
    """
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")  # 启用外键约束
    cursor = conn.cursor()

    # 创建项目表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE,
        city TEXT NOT NULL,
        scale TEXT NOT NULL,
        type TEXT NOT NULL
    );
    """)

    # 创建日志表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Logs (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        city TEXT NOT NULL,
        task TEXT NOT NULL,
        user_id INTEGER,
        weather TEXT,
        FOREIGN KEY (project_id) REFERENCES Projects (project_id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE SET NULL
    );
    """)

    # 创建任务表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Tasks (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        log_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        content TEXT NOT NULL,
        comment TEXT,
        status TEXT DEFAULT '未完成',
        FOREIGN KEY (log_id) REFERENCES Logs (log_id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES Projects (project_id) ON DELETE CASCADE
    );
    """)

    # 创建任务频度表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS TasksHistory (
        task_id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL UNIQUE,
        frequency INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # 创建天气表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Weather (
        weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        temperature REAL,
        wind_speed REAL,
        humidity REAL,
        description TEXT,
        FOREIGN KEY (project_id) REFERENCES Projects (project_id) ON DELETE CASCADE
    );
    """)

    # 创建用户表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    # 创建用户-项目表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users_Projects (
        user_project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        project_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users (user_id) ON DELETE CASCADE,
        FOREIGN KEY (project_id) REFERENCES Projects (project_id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()
    print("数据库已成功初始化！")

if __name__ == "__main__":
    initialize_database()
