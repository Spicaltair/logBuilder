# utils/history_manager.py

import json
import os

HISTORY_FILE = "history.json"

def save_history(selected_city):
    """
    将用户选择保存到历史记录文件
    """
    history = {"last_selected_city": selected_city}
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f)

def load_history():
    """
    加载用户历史选择
    """
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
            return history.get("last_selected_city", None)
    return None
