import pyautogui
import keyboard

def get_mouse_info():
    """
    获取并打印当前鼠标的坐标和像素颜色。
    """
    try:
        # 获取当前鼠标的x和y坐标
        x, y = pyautogui.position()

        # 获取当前鼠标位置的像素颜色
        pixel_color = pyautogui.pixel(x, y - 5)

        # 格式化输出
        position_str = f"鼠标坐标: ({x},{y}) 修正 {y - 5}"
        color_str = f"像素颜色: {pixel_color}"

        print(f"{position_str} | {color_str}")

    except Exception as e:
        print(f"发生错误: {e}")

print("脚本已启动。按 'u' 键获取鼠标信息，按 'q' 键退出。")

# 绑定 'u' 键到 get_mouse_info 函数
keyboard.add_hotkey('u', get_mouse_info)

# 等待 'q' 键被按下以退出程序
keyboard.wait('q')

print("脚本已退出。")