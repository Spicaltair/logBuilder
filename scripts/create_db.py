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

# 创建表的 SQL 语句
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
conn.commit()
conn.close()

print("数据库表已成功创建！")
