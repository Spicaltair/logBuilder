# LogBuilder

LogBuilder 是一个用于日志管理和项目综合信息展示的桌面应用程序，专为工程项目管理者设计，帮助用户高效记录和跟踪工作内容。

---

## 功能特色

1. **日期管理**
   - 提供日历选择器，方便快速选择和记录日期。
   - 支持自定义日期备注。

2. **城市天气**
   - 实时获取和显示指定城市的天气信息。
   - 天气信息包括温度、湿度、风速等。

3. **任务管理**
   - 增加、编辑和删除任务。
   - 支持任务优先级管理。
   - 数据库存储，确保任务持久保存。

4. **项目管理**
   - 管理项目阶段性进展。
   - 提供便捷的项目信息存储和检索功能。

5. **用户管理**
   - 添加和维护用户信息。
   - 管理权限和基本信息。

---

## 安装说明

### 环境要求
- Windows 10 或以上操作系统。
- 无需安装 Python 环境，直接运行打包后的可执行文件。

### 下载
请访问 [GitHub 项目主页](https://github.com/Spicaltair/logBuilder) 下载最新版本的可执行文件。

### 运行
1. 解压下载的压缩包。
2. 双击 `LogBuilder.exe` 即可启动程序。

---

## 使用指南

### 初次启动
- 默认会加载日期和默认城市的天气信息。
- 用户可以在不同的标签页中切换，进行日期管理、任务编辑等操作。

### 数据存储
- 所有任务和项目管理数据均存储在本地 SQLite 数据库中。
- 确保程序目录具有写权限，以便保存修改。

---

## 常见问题

### 1. 启动时报错 `ModuleNotFoundError: No module named 'babel.numbers'`
   **解决办法**：
   - 确保运行的是打包后的可执行文件。
   - 如果自行打包，请使用以下命令：
     ```bash
     pyinstaller --hidden-import babel.numbers logbuilder.py
     ```

### 2. 数据库问题 `no such table: tasks`
   **解决办法**：
   - 确保 `tasks.db` 文件存在且完整。
   - 检查程序运行目录是否具有写权限。

---

## 开发者

LogBuilder 是由 [Spicaltair](https://github.com/Spicaltair) 开发和维护的项目。

---

## 贡献
欢迎提交 issue 或 pull request 来改进 LogBuilder。详细信息请参阅 [CONTRIBUTING.md](https://github.com/Spicaltair/logBuilder/blob/main/CONTRIBUTING.md)。

---

## 许可证

此项目基于 [MIT License](https://github.com/Spicaltair/logBuilder/blob/main/LICENSE) 开源。

