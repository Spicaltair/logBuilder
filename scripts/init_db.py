import os
import sqlite3

# 获取当前脚本所在目录的父级目录
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 指定数据库文件的存储路径
db_path = os.path.join(base_dir, 'data', 'construction_logs.db')

# 确保 data 目录存在
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# 创建数据库连接
conn = sqlite3.connect(db_path)
cursor = conn.cursor()




def initialize_database():
    """
    初始化 SQLite 数据库，创建必要的表
    """
    conn = sqlite3.connect('data/construction_logs.db')
    cursor = conn.cursor()


    # 创建项目表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        start_date DATE,
        end_date DATE,
        manager TEXT
    );
    """)
    
    # 创建日志表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER,
        date TEXT NOT NULL,
        city TEXT NOT NULL,
        task TEXT NOT NULL,
        weather TEXT
    );
    ''')
    
    # 创建任务表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            date DATE NOT NULL,
            status TEXT DEFAULT '未完成',
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES Projects (project_id)
        )
    ''')
    # 创建任务频度表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TasksHistory (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL UNIQUE,
            frequency INTEGER DEFAULT 0, 
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')   
    
    # 创建 Weather 表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            temperature REAL,
            wind_speed REAL,
            humidity REAL,
            description TEXT,
            project_id INTEGER,
            FOREIGN KEY (project_id) REFERENCES Projects (id)
        )
    ''')    
    
     # 创建用户表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')   
    
    conn.commit()
    conn.close()
    print("数据库已成功初始化！")

if __name__ == "__main__":
    initialize_database()
