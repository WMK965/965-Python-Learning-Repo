import pyautogui
import keyboard
import time

# ------------------- 配置中心 -------------------
# 在此区域集中管理所有可配置的参数
CONFIG = {
    # -- 基本设置 --
    'screen_height': 1440,              # 屏幕的垂直分辨率
    'fish_timeout': 30,                 # 钓鱼等待超时时间（秒）
    'color_tolerance': 20,              # 颜色相似度比较的容差值

    # -- 坐标与颜色 --
    'toolbar_detection': {
        'color': (255, 228, 161),       # 用于检测物品栏位置的颜色
        'top_pos': (1280, 60),          # 物品栏在上方时的检测点
        'bottom_pos': (1280, 1380)      # 物品栏在下方时的检测点
    },
    'stamina': {
        'check_pos': (2529, 1406),      # 体力条检测点
        'low_stamina_color': (248, 189, 117) # 体力不足时的颜色
    },
    'fishing_rod': {
        'hook_check_pos_b': (1275, 580),  # 鱼上钩的感叹号检测点
        'hook_check_pos_t': (1275, 680),
        'hooked_color': (199, 183, 223),# 鱼上钩时的颜色
        'bar_pos_x': 930                # 钓竿在物品栏的X坐标
    },
    'food': {
        'check_color': (241, 174, 100), # 食物图标的检测颜色
        'check_pos_x': 1280,            # 食物检测点的X坐标
        'bar_pos_x_1': 1565,            # 第一个食物栏位的X坐标
        'bar_pos_x_2': 1630,            # 第二个食物栏位的X坐标
        'check_y': 1185,         # 食物检测点
        'click_y': 1270          # 食物点击点
    },
    'toolbar_y': {
        'bottom': 1395,                 # 物品栏在下方时的基准Y坐标
    },
    
    # -- 延时设置 (秒) --
    'delays': {
        'action_interval': 0.2,         # 连续鼠标操作之间的间隔
        'post_eat': 1.5,                # 吃完食物后的等待时间
        'post_action': 0.8,             # 执行动作后的通用等待时间
        'cast_rod_hold': 0.92,          # 抛竿按住左键的时间
        'post_cast': 1.0,               # 抛竿后的等待时间
        'post_catch': 3.0,              # 成功收杆后的等待时间
        'loop_interval': 1.0,           # 每个大循环结束后的休息时间
        'cpu_rest': 0.1                 # 脚本暂停时的循环等待时间
    }
}
# ------------------- 函数定义 -------------------

def are_colors_similar(color1, color2, tolerance=CONFIG['color_tolerance']):
    """
    比较两种RGB颜色是否在指定的容差范围内相似。
    """
    if not all(isinstance(c, (tuple, list)) and len(c) == 3 for c in [color1, color2]):
        return False

    r1, g1, b1 = color1
    r2, g2, b2 = color2
    return (abs(r1 - r2) <= tolerance and
            abs(g1 - g2) <= tolerance and
            abs(b1 - b2) <= tolerance)


def detect_toolbar_position():
    """
    检测物品栏是在屏幕上方还是下方。
    返回 'TOP', 'BOTTOM', 或 None。
    """
    try:
        # 检测下方位置
        if are_colors_similar(pyautogui.pixel(*CONFIG['toolbar_detection']['bottom_pos']), CONFIG['toolbar_detection']['color']):
            return 'BOTTOM'
        # 检测上方位置
        if are_colors_similar(pyautogui.pixel(*CONFIG['toolbar_detection']['top_pos']), CONFIG['toolbar_detection']['color']):
            return 'TOP'
    except Exception as e:
        print(f"检测物品栏位置时出错: {e}")
    
    print("错误：未能检测到物品栏位置。")
    return None


def check_stamina():
    """
    步骤1：检查体力是否需要补充。
    返回 True 如果体力不足，否则返回 False。
    """
    try:
        current_color = pyautogui.pixel(*CONFIG['stamina']['check_pos'])
        target_color = CONFIG['stamina']['low_stamina_color']
        print(f"检查体力... 目标颜色: {target_color}, 当前颜色: {current_color}")
        
        if are_colors_similar(current_color, target_color):
            print("结果：体力不足，需要补充。")
            return True
        else:
            print("结果：体力充足。")
            return False
    except Exception as e:
        print(f"检查体力时发生错误: {e}")
        return False


def replenish_stamina(toolbar_pos):
    """
    步骤2：执行补充体力的操作。
    返回 True 如果成功补充，否则返回 False。
    """
    print("开始补充体力...")

    # 根据物品栏位置确定Y坐标
    base_y = CONFIG['toolbar_y']['bottom']
    if toolbar_pos == 'TOP':
        # 上方布局的Y坐标是对称的
        base_y = CONFIG['screen_height'] - base_y

    # 尝试第一个食物栏位
    pyautogui.moveTo(CONFIG['food']['bar_pos_x_1'], base_y, duration=CONFIG['delays']['action_interval']) # Bar
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')
    time.sleep(CONFIG['delays']['action_interval'])
    pyautogui.moveTo(200, 200, duration=CONFIG['delays']['action_interval'])
    time.sleep(CONFIG['delays']['post_action'])
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')
    time.sleep(CONFIG['delays']['post_action'])

    if are_colors_similar(pyautogui.pixel(CONFIG['food']['check_pos_x'], CONFIG['food']['check_y']), CONFIG['food']['check_color']):
        print("检测到食物")
        pyautogui.moveTo(CONFIG['food']['check_pos_x'], CONFIG['food']['click_y'], duration=CONFIG['delays']['action_interval'])
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')
        print("已使用食物")
        time.sleep(CONFIG['delays']['post_eat'])
        return True

    print("未在当前栏位找到食物")
    time.sleep(CONFIG['delays']['post_action'])

    # 尝试第二个食物栏位
    pyautogui.moveTo(CONFIG['food']['bar_pos_x_2'], base_y, duration=CONFIG['delays']['action_interval']) # Bar
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')
    time.sleep(CONFIG['delays']['action_interval'])
    pyautogui.moveTo(200, 200, duration=CONFIG['delays']['action_interval'])
    pyautogui.mouseDown(button='right')
    pyautogui.mouseUp(button='right')
    time.sleep(CONFIG['delays']['post_action'])

    if are_colors_similar(pyautogui.pixel(CONFIG['food']['check_pos_x'], CONFIG['food']['check_y']), CONFIG['food']['check_color']):
        print("在切换后的栏位检测到食物")
        pyautogui.moveTo(CONFIG['food']['check_pos_x'], CONFIG['food']['click_y'], duration=CONFIG['delays']['action_interval'])
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')
        print("已使用食物")
        time.sleep(CONFIG['delays']['post_eat'])
        return True

    print("错误：两次尝试均未找到指定食物，脚本将进入等待状态")
    return False


def go_fishing(toolbar_pos):
    """
    执行一次完整的钓鱼流程。
    """
    print("\n----- 开始新一轮钓鱼 -----")
    
    # 根据物品栏位置确定Y坐标
    base_y = CONFIG['toolbar_y']['bottom']
    hook_check_pos = CONFIG['fishing_rod']['hook_check_pos_b']
    if toolbar_pos == 'TOP':
        base_y = CONFIG['screen_height'] - base_y
        hook_check_pos = CONFIG['fishing_rod']['hook_check_pos_t']

    # 步骤3：抛竿
    time.sleep(CONFIG['delays']['post_cast'])
    pyautogui.moveTo(CONFIG['fishing_rod']['bar_pos_x'], base_y, duration=CONFIG['delays']['action_interval']) #Bar
    pyautogui.mouseDown(button='left')
    pyautogui.mouseUp(button='left')
    time.sleep(CONFIG['delays']['action_interval'])
    pyautogui.moveTo(200, 200, duration=CONFIG['delays']['action_interval'])
    print("抛竿...")
    time.sleep(CONFIG['delays']['post_cast'])
    pyautogui.mouseDown(button='left')
    time.sleep(CONFIG['delays']['cast_rod_hold'])
    pyautogui.mouseUp(button='left')
    print("已抛竿，等待上钩...")

    # 步骤4：循环检测鱼是否上钩
    start_time = time.time()
    fish_hooked = False
    
    while time.time() - start_time < CONFIG['fish_timeout']:
        try:
            current_color = pyautogui.pixel(*hook_check_pos)
            if are_colors_similar(current_color, CONFIG['fishing_rod']['hooked_color']):
                print(f"鱼上钩了！当前颜色: {current_color}")
                fish_hooked = True
                break
        except Exception as e:
            print(f"检测鱼上钩时出错: {e}")
        time.sleep(1)

    # 步骤5：收杆
    if fish_hooked:
        print("收杆！单击左键")
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')
        time.sleep(CONFIG['delays']['post_catch'])
    else:
        print(f"{CONFIG['fish_timeout']}秒内未检测到鱼上钩，将开始下一轮循环")


# ------------------- 主程序与热键控制 -------------------
running = False
exit_program = False

def toggle_script_state():
    global running
    running = not running
    if running:
        print("\n========= 脚本已启动 =========")
    else:
        print("\n========= 脚本已暂停 =========")

def quit_program():
    global running, exit_program
    running = False
    exit_program = True
    print("\n程序即将退出...")

def main():
    """
    主函数，包含脚本的主要循环。
    """
    print("自动化脚本已准备就绪。")
    print("--------------------------------")
    print("  按 '3' 键来【启动 / 暂停】脚本")
    print("  按 '9' 键来【退出】整个程序")
    print("  手动调整位置：钓竿位于1号位")
    print("              食物位于 - = 位")
    print("--------------------------------")

    keyboard.add_hotkey('3', toggle_script_state)
    keyboard.add_hotkey('9', quit_program)

    while not exit_program:
        if running:
            # 0. 检测物品栏位置
            toolbar_position = detect_toolbar_position()
            if not toolbar_position:
                print("无法确定物品栏位置，自动暂停脚本。")
                toggle_script_state()
                continue
            
            # 1. 检查体力
            if check_stamina():
                # 2. 体力不足，进行补充
                if not replenish_stamina(toolbar_position):
                    toggle_script_state()
                    print("请手动处理后按 '3' 再次启动。")
            else:
                # 3. 体力充足，去钓鱼
                go_fishing(toolbar_position)

            time.sleep(CONFIG['delays']['loop_interval'])
        else:
            time.sleep(CONFIG['delays']['cpu_rest'])

    print("主循环已结束。")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"发生未预料的错误: {e}")
    finally:
        print("程序已完全关闭。")