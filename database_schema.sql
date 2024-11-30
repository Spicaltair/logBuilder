<<<<<<< HEAD
=======

CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY, -- 用户唯一标识
    username VARCHAR(50) NOT NULL,         -- 用户名
    email VARCHAR(100) NOT NULL UNIQUE,    -- 邮箱
    password_hash VARCHAR(255) NOT NULL,   -- 加密后的密码
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP -- 更新时间
);

>>>>>>> d8952c9 (Apply changes from nested directory)
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    manager TEXT
);
CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    date DATE NOT NULL,
    progress REAL,
    summary TEXT,
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
);
CREATE TABLE tasks_materials (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,
    task_description TEXT,
    material_name TEXT,
    material_quantity REAL,
    unit TEXT,
    FOREIGN KEY (log_id) REFERENCES logs (log_id)
);
CREATE TABLE issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,
    description TEXT,
    status TEXT,
    resolved_date DATE,
    FOREIGN KEY (log_id) REFERENCES logs (log_id)
);
CREATE TABLE attachments (
    attachment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,
    file_path TEXT,
    upload_date DATE,
    file_type TEXT,
    FOREIGN KEY (log_id) REFERENCES logs (log_id)
);
CREATE TABLE weather (
    weather_id INTEGER PRIMARY KEY AUTOINCREMENT,
    log_id INTEGER NOT NULL,
    temperature REAL,
    wind_direction REAL,
    wind_speed REAL,
    humidity REAL,
    precipitation REAL,
    weather_condition TEXT,
    visibility REAL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (log_id) REFERENCES logs (log_id)
);
