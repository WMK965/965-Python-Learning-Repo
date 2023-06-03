import pyautogui

# 获取屏幕分辨率
screen_width, screen_height = pyautogui.size()

# 获取按钮的坐标
button_x, button_y = pyautogui.locateCenterOnScreen('button.png')

# 移动鼠标到按钮的位置
pyautogui.moveTo(button_x, button_y)

# 单击按钮
pyautogui.click()
