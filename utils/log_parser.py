def read_log_file(filepath):
    """
    读取日志文件内容。

    Args:
        filepath (str): 日志文件路径。

    Returns:
        str: 日志文件的内容。
    """
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
