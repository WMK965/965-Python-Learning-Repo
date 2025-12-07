import psutil
import json
import time
import datetime
from screeninfo import get_monitors


def get_monitor_count():
    """
    获取当前激活的显示器数量。

    Returns:
        int: 激活的显示器数量。
    """
    try:
        return len(get_monitors())
    except Exception as e:
        print(f"无法检测显示器: {e}")
        return 0


def get_high_cpu_processes(monitor_count):
    """
    获取 CPU 占用率超过 3% 的进程信息，并排除 PID 0。

    Args:
        monitor_count (int): 当前激活的显示器数量。

    Returns:
        list: 包含高 CPU 占用率进程信息的字典列表。
    """
    processes = []
    # 初始化 psutil 的 cpu_percent，以便后续调用能立即返回有意义的值
    psutil.cpu_percent()
    time.sleep(0.1)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            # 排除 System Idle Process (PID 0)
            if proc.info['pid'] == 0:
                continue

            cpu_percent = proc.cpu_percent()
            if cpu_percent >= 3.0:
                process_info = {
                    'timestamp': datetime.datetime.now().isoformat(),
                    'pid': proc.info['pid'],
                    'name': proc.info['name'],
                    'cpu_percent': cpu_percent,
                    'monitor_count': monitor_count
                }
                processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return processes


def write_to_json(data, filename="process_log.json"):
    """
    将数据追加到标准的 JSON 文件中。如果文件不存在，则创建它。

    Args:
        data (list): 要写入的进程信息列表。
        filename (str, optional): 输出的 JSON 文件名。默认为 "process_log.json"。
    """
    if not data:  # 如果没有新数据，则不执行任何操作
        return

    try:
        with open(filename, 'r+', encoding='utf-8') as file:
            # 读取现有数据，如果文件为空则初始化为空列表
            try:
                file_data = json.load(file)
            except json.JSONDecodeError:
                file_data = []

            # 追加新数据
            file_data.extend(data)
            # 将文件指针移回开头以覆盖文件
            file.seek(0)
            # 写入更新后的数据
            json.dump(file_data, file, indent=4)
    except FileNotFoundError:
        # 如果文件不存在，则创建新文件并写入数据
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4)


if __name__ == "__main__":
    while True:
        active_monitors = get_monitor_count()
        print(f"正在监控... | 当前激活的显示器数量: {active_monitors}")

        high_cpu_processes = get_high_cpu_processes(active_monitors)

        if high_cpu_processes:
            print(f"发现 {len(high_cpu_processes)} 个 CPU 占用率 > 3% 的进程。正在记录到 process_log.json...")
            write_to_json(high_cpu_processes)
        else:
            print("未发现 CPU 占用率 > 3% 的进程。")

        time.sleep(10)
