import sqlite3

def initialize_database():
    """
    初始化 SQLite 数据库，创建必要的表
    """
    conn = sqlite3.connect('data/construction_logs.db')
    cursor = conn.cursor()

    # 创建日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            city TEXT NOT NULL,
            task TEXT NOT NULL,
            weather TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("数据库已成功初始化！")

if __name__ == "__main__":
    initialize_database()
