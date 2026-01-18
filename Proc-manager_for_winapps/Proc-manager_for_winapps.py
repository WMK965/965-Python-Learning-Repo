import psutil
import subprocess
import sys
import os
import time


def start_program(args):
    """
    启动程序并返回 psutil.Process 对象
    """
    try:
        # 获取可执行文件的目录，将其设为工作目录 (cwd)
        # 很多程序（如百度网盘）如果不在自身目录下运行，会报错或缺DLL
        exe_path = os.path.abspath(args[0])
        work_dir = os.path.dirname(exe_path)

        print(f"[*] 正在启动: {exe_path}")
        print(f"[*] 工作目录: {work_dir}")

        # 使用 subprocess 启动
        # args 是一个列表，例如 ['C:/.../exe', '-arg1']
        p = subprocess.Popen(args, cwd=work_dir, shell=False)

        # 暂停一小会儿，让程序有时间初始化并创建子进程
        time.sleep(1)

        # 将 subprocess 对象转换为 psutil 对象，以便进行高级操作
        return psutil.Process(p.pid)

    except FileNotFoundError:
        print(f"[!] 错误: 找不到文件 {args[0]}")
        return None
    except Exception as e:
        print(f"[!] 启动失败: {e}")
        return None


def list_children(parent_proc):
    """
    列出所有子进程
    """
    try:
        children = parent_proc.children(recursive=True)
        if not children:
            print("[-] 当前没有检测到子进程。")
            return []

        print(f"\n[+] 发现 {len(children)} 个子进程 (父进程 PID: {parent_proc.pid}):")
        print(f"{'PID':<10} {'名称':<25} {'状态':<10} {'内存(MB)':<10}")
        print("-" * 60)

        for child in children:
            try:
                mem = child.memory_info().rss / 1024 / 1024
                print(f"{child.pid:<10} {child.name()[:25]:<25} {child.status():<10} {mem:.2f}")
            except psutil.NoSuchProcess:
                continue
        print("-" * 60)
    except psutil.NoSuchProcess:
        print("[!] 主进程已结束。")


def kill_process(pid):
    """
    终止指定PID
    """
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate()
        proc.wait(timeout=3)
        print(f"[+] 进程 {name} (PID: {pid}) 已终止。")
    except psutil.NoSuchProcess:
        print(f"[!] 进程 {pid} 不存在。")
    except Exception as e:
        print(f"[!] 无法终止进程: {e}")


def kill_tree(parent_proc, kill_root=False):
    """
    终止进程树
    :param kill_root: 是否连同父进程一起杀掉
    """
    try:
        children = parent_proc.children(recursive=True)
        for child in children:
            kill_process(child.pid)

        if kill_root:
            kill_process(parent_proc.pid)
            print("[+] 主程序已终止。")
    except psutil.NoSuchProcess:
        print("[!] 主进程已不存在。")


def main():
    if len(sys.argv) < 2:
        print("使用方法: python app_launcher.py <exe路径> [参数...]")
        print(r"示    例: python app_launcher.py C:\Users\965\...\BaiduNetdisk.exe")
        return

    # sys.argv[1:] 包含了 exe 路径和它后面可能跟的所有参数
    target_args = sys.argv[1:]

    # 1. 启动程序
    main_proc = start_program(target_args)

    if not main_proc:
        return

    print(f"[+] 程序已启动，PID: {main_proc.pid}")
    print("[*] 进入监控模式...")

    # 2. 交互循环
    while True:
        try:
            # 检查主进程是否存活
            if not psutil.pid_exists(main_proc.pid):
                print("\n[!] 检测到主程序已退出。工具结束。")
                break

            # 获取用户输入
            cmd_input = input("\n(监控中) 指令 [ls | kill <pid> | killall | killmain | exit] > ").strip().lower()

            if cmd_input == 'ls':
                list_children(main_proc)

            elif cmd_input.startswith('kill '):
                try:
                    pid = int(cmd_input.split()[1])
                    kill_process(pid)
                except:
                    print("[!] 格式错误: kill <pid>")

            elif cmd_input == 'killall':
                print("[*] 正在清理子进程...")
                kill_tree(main_proc, kill_root=False)

            elif cmd_input == 'killmain':
                if input("确定关闭主程序吗? (y/n): ").lower() == 'y':
                    kill_tree(main_proc, kill_root=True)
                    break

            elif cmd_input == 'exit':
                print("退出监控工具 (主程序将继续运行)。")
                break

            else:
                print("[!] 未知指令")

        except KeyboardInterrupt:
            print("\n[!] 强制退出。")
            break
        except psutil.NoSuchProcess:
            print("[!] 主进程丢失。")
            break


if __name__ == "__main__":
    main()