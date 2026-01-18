import psutil
import subprocess
import sys
import os
import time
import ctypes
from ctypes import wintypes

# --- Windows API 定义 ---
user32 = ctypes.WinDLL('user32', use_last_error=True)
SW_MINIMIZE = 6
SW_RESTORE = 9


def set_window_state(pid, state_cmd):
    """
    设置窗口状态 (最小化/还原)
    """
    # 定义回调函数类型: bool(HWND, LPARAM)
    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, wintypes.HWND, wintypes.LPARAM)

    target_hwnds = []

    # 内部回调函数 (闭包)
    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            window_pid = ctypes.c_ulong()
            user32.GetWindowThreadProcessId(hwnd, ctypes.byref(window_pid))
            if window_pid.value == pid:
                target_hwnds.append(hwnd)
        return True

    # 调用 EnumWindows，参数2传0即可
    user32.EnumWindows(WNDENUMPROC(callback), 0)

    if not target_hwnds:
        print(
            f"[!] 未找到 PID {pid} 的可见窗口 (可能窗口属于子进程，请尝试 'ls' 查看子进程PID并手动修改代码逻辑，或窗口被隐藏)。")
        return

    for hwnd in target_hwnds:
        user32.ShowWindow(hwnd, state_cmd)

    action = "最小化" if state_cmd == SW_MINIMIZE else "还原"
    print(f"[+] 已{action} PID {pid} 的窗口。")


# --- 核心逻辑 ---

def start_program(args):
    try:
        exe_path = os.path.abspath(args[0])
        work_dir = os.path.dirname(exe_path)
        print(f"[*] 启动引导程序: {exe_path}")
        # 使用 shell=False 确保能拿到准确的 PID
        p = subprocess.Popen(args, cwd=work_dir, shell=False)
        return psutil.Process(p.pid)
    except Exception as e:
        print(f"[!] 启动失败: {e}")
        return None


def smart_handover(proc):
    """
    智能交接：如果主进程是启动器(Launcher)，则追踪其真正的子进程
    """
    print("[*] 进入启动追踪模式 (等待 5 秒观察进程行为)...")

    start_time = time.time()
    potential_heir = None

    while time.time() - start_time < 8:
        try:
            # 1. 检查子进程
            children = proc.children(recursive=False)
            if children:
                potential_heir = children[-1]

            # 2. 检查主进程状态
            if proc.status() == psutil.STATUS_ZOMBIE or not proc.is_running():
                print(f"[-] 引导进程 (PID: {proc.pid}) 已退出。")
                if potential_heir and potential_heir.is_running():
                    print(f"[!] 发现接班进程: {potential_heir.name()} (PID: {potential_heir.pid})")
                    print("[+] 切换监控目标 -> 接班进程")
                    return potential_heir
                else:
                    print("[!] 引导进程退出了，且没有发现存活的子进程。")
                    return None

            time.sleep(0.5)

        except psutil.NoSuchProcess:
            if potential_heir and potential_heir.is_running():
                return potential_heir
            return None

    print(f"[+] 引导进程 (PID: {proc.pid}) 运行稳定，将其作为主监控目标。")
    return proc


def list_children(parent_proc):
    try:
        children = parent_proc.children(recursive=True)
        print(f"\n[+] 进程树 (主PID: {parent_proc.pid}):")
        print(f"{'PID':<10} {'名称':<25} {'内存(MB)':<10}")
        print("-" * 50)

        try:
            mem = parent_proc.memory_info().rss / 1024 / 1024
            print(f"{parent_proc.pid:<10} {parent_proc.name()[:25]:<25} {mem:.2f} (Main)")
        except:
            pass

        for child in children:
            try:
                mem = child.memory_info().rss / 1024 / 1024
                print(f"{child.pid:<10} {child.name()[:25]:<25} {mem:.2f}")
            except:
                continue
        print("-" * 50)
    except psutil.NoSuchProcess:
        print("[!] 进程已结束。")


def kill_tree(parent_proc):
    try:
        children = parent_proc.children(recursive=True)
        for child in children:
            try:
                child.terminate()
            except:
                pass
        parent_proc.terminate()
        print("[+] 已终止进程树。")
    except:
        print("[!] 进程已不存在。")


def main():
    if len(sys.argv) < 2:
        print("用法: python advanced_monitor.py <exe路径> [参数...]")
        return

    # 1. 启动
    initial_proc = start_program(sys.argv[1:])
    if not initial_proc: return

    # 2. 智能交接
    main_proc = smart_handover(initial_proc)

    if not main_proc:
        print("[!] 目标丢失，程序结束。")
        return

    print(f"\n[*] 正在监控: {main_proc.name()} (PID: {main_proc.pid})")
    print("指令: [ls]列出进程 | [min]最小化 | [max]还原 | [kill]终止 | [exit]退出")

    # 3. 循环监控
    while True:
        try:
            if not main_proc.is_running():
                print("\n[!] 主程序已退出。")
                break

            cmd = input("\n指令 > ").strip().lower()

            if cmd == 'ls':
                list_children(main_proc)
            elif cmd == 'min':
                set_window_state(main_proc.pid, SW_MINIMIZE)
            elif cmd == 'max':
                set_window_state(main_proc.pid, SW_RESTORE)
            elif cmd == 'kill':
                if input("确认终止? (y/n): ").lower() == 'y':
                    kill_tree(main_proc)
                    break
            elif cmd == 'exit':
                break
            else:
                print("未知指令")

        except KeyboardInterrupt:
            break
        except psutil.NoSuchProcess:
            print("[!] 进程丢失。")
            break


if __name__ == "__main__":
    main()