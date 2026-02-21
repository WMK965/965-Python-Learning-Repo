import os
import sys
import time
import yaml
import subprocess
import argparse
from pathlib import Path


def get_base_path():
    """获取程序运行时的真实根目录（兼容 PyInstaller）"""
    if getattr(sys, 'frozen', False):
        # 如果是打包后的 exe，返回 exe 所在的文件夹
        return Path(sys.executable).parent
    else:
        # 如果是脚本运行，返回脚本所在的文件夹
        return Path(__file__).parent


class StartupManager:
    def __init__(self, config_path=None):
        # 如果命令行没指定，默认在程序同级目录下叫 startup_config.yaml
        self.config_file = Path(config_path) if config_path else get_base_path() / "startup_config.yaml"
        self.config = self._load_config()

    def _load_config(self):
        if not self.config_file.exists():
            return {"apps": {}}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {"apps": {}}
                return self._auto_correct(data)
        except Exception as e:
            print(f"读取配置失败，初始化新配置: {e}")
            return {"apps": {}}

    def _auto_correct(self, data):
        """自动修正：根据优先级排序并重新生成连续编号 'no'"""
        if "apps" not in data or not data["apps"]:
            return data

        # 1. 提取所有项并排序 (先按优先级 priority，再按名称字母)
        items = []
        for name, info in data["apps"].items():
            info['name'] = name  # 临时存储名称方便排序
            items.append(info)

        items.sort(key=lambda x: (x.get('priority', 99), x['name']))

        # 2. 重新分配编号并写回字典
        new_apps = {}
        for index, item in enumerate(items, start=1):
            name = item.pop('name')
            item['no'] = index  # 自动修正编号
            new_apps[name] = item

        data["apps"] = new_apps
        return data

    def _save_config(self):
        # 保存前再次执行修正
        self.config = self._auto_correct(self.config)
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                yaml.dump(self.config, f, allow_unicode=True, sort_keys=False)
        except Exception as e:
            print(f"保存配置文件失败: {e}")

    def add_app(self, name, path, args, priority, delay):
        self.config["apps"][name] = {
            "path": path,
            "args": args or [],
            "priority": priority,
            "delay": delay,
            "enabled": True
        }
        self._save_config()
        print(f"成功注册并修正编号: {name}")

    def del_app(self, name_or_no):
        """支持通过名称或编号删除"""
        target_name = None
        for name, info in self.config["apps"].items():
            if name == name_or_no or str(info.get('no')) == str(name_or_no):
                target_name = name
                break

        if target_name:
            del self.config["apps"][target_name]
            self._save_config()
            print(f"已删除并重新整理编号: {target_name}")
        else:
            print(f"错误: 未找到项 '{name_or_no}'")

    def list_apps(self):
        apps = self.config.get("apps", {})
        if not apps:
            print(f"启动列表为空。(配置文件: {self.config_file})")
            return

        print(f"\n配置文件位置: {self.config_file}")
        print(f"{'No.':<4} {'名称':<15} {'优先级':<8} {'延迟(s)':<8} {'状态':<6} {'命令行'}")
        print("-" * 90)

        # 已经是修正过的，直接按 no 排序显示
        sorted_apps = sorted(apps.items(), key=lambda x: x[1]['no'])
        for name, info in sorted_apps:
            status = "ON" if info.get("enabled", True) else "OFF"
            cmd = f"{info['path']} {' '.join(info['args'])}"
            print(f"{info.get('no', '?'):<4} {name:<15} {info['priority']:<10} {info['delay']:<10} {status:<6} {cmd}")

    def run_startup(self):
        apps = self.config.get("apps", {})
        enabled_apps = sorted(
            [(n, i) for n, i in apps.items() if i.get("enabled", True)],
            key=lambda x: x[1]['no']
        )

        if not enabled_apps:
            print("没有需要启动的任务。")
            return

        # 准备一个干净的环境变量副本，移除 PyInstaller 的临时路径标记
        clean_env = os.environ.copy()
        clean_env.pop("_MEIPASS", None)

        print(f"[{time.strftime('%H:%M:%S')}] 启动序列开始...")
        for name, info in enabled_apps:
            delay = info.get("delay", 0)
            if delay > 0:
                # 这里的打印能让你确认 delay 是否生效
                print(f"[{time.strftime('%H:%M:%S')}] 等待 {delay}s 后启动 {name}...")
                time.sleep(delay)

            try:
                raw_args = info.get('args', [])
                processed_args = [a.strip() for a in raw_args]
                cmd = [info['path']] + processed_args

                # 增加 env=clean_env 和 close_fds=True
                subprocess.Popen(
                    cmd,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    stdin=subprocess.DEVNULL,
                    env=clean_env,  # 关键：切断与临时目录的联系
                    close_fds=True,  # 关键：关闭继承的句柄
                    shell=False,
                    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
                )
                print(f"[{time.strftime('%H:%M:%S')}] 已成功拉起: {name}")
            except Exception as e:
                print(f"启动失败 {name}: {e}")

        # 给系统一点点时间处理句柄释放，防止主进程退出太快
        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(description="BootMaster Pro")
    parser.add_argument("-c", "--config", type=str, help="指定配置文件路径 (可选)")
    parser.add_argument("--run", action="store_true", help="执行启动序列")
    parser.add_argument("--list", action="store_true", help="列出启动项")
    parser.add_argument("--reg", type=str, metavar="NAME", help="注册新启动项名称")
    parser.add_argument("--path", type=str, help="程序完整路径")
    parser.add_argument("--args", type=str, help="所有启动参数，请放在引号内，如 ' -silent -min'")
    parser.add_argument("--prio", type=int, default=10, help="优先级 (1-99)")
    parser.add_argument("--delay", type=int, default=0, help="延迟秒数")
    parser.add_argument("--del-item", type=str, metavar="NAME_OR_NO", help="删除启动项(支持名称或编号)")

    args = parser.parse_args()
    manager = StartupManager(config_path=args.config)

    if args.run:
        manager.run_startup()
    elif args.list:
        manager.list_apps()
    elif args.reg:
        if not args.path:
            print("错误: 必须提供 --path")
        else:
            arg_list = args.args.split() if args.args else []
            manager.add_app(args.reg, args.path, arg_list, args.prio, args.delay)
    elif args.del_item:
        manager.del_app(args.del_item)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()