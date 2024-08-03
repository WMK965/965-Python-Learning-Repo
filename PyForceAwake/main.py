import pyautogui
import time
import os

# basePATH
screenWidth, screenHeight = pyautogui.size()
currentMouseX, currentMouseY = pyautogui.position()
loop = 1
time_set = 0


while True:
    inp = int(input('''*****************************************
**          当前时间 {0}          **
*****************************************
** 扣1继续 | 扣2设置时间(%H:%M & min)  **
*****************************************
'''.format(time.strftime("%H:%M:%S", time.localtime()))))

    if inp == 1:

        while loop > 0:
            print("[INFO][{0}] Moving...".format(time.strftime("%H:%M:%S", time.localtime())))
            pyautogui.moveTo(1280, 720)
            time.sleep(4)
            pyautogui.moveTo(1920, 1080, duration=2)
            pyautogui.click()
            time.sleep(594)
            print("[INFO][{0}] Loop {1} Ended".format(time.strftime("%H:%M:%S", time.localtime()), loop))
            loop = loop - 1

        if time_set == 1:
            os.system("shutdown -s -t 60")

        break

    elif inp == 2:
        target = input()
        time_set = 1
        local_min = 60 * int(time.strftime("%H:%M", time.localtime()).split(":")[0]) + int(time.strftime("%H:%M", time.localtime()).split(":")[1])

        try:
            target_min = 60 * int(target.split(":")[0]) + int(target.split(":")[1])
            if target_min > local_min:
                loop = (target_min - local_min) // 10
            elif 0 < target_min - local_min < 10:
                loop = 1
            elif local_min - target_min > 720:
                loop = (target_min - local_min + 1440) // 10
            elif local_min - target_min <= 720:
                loop = (target_min - local_min + 720) // 10

        except IndexError:
            target = int(target)
            if 0 < target < 10:
                loop = 1
            elif target > 10:
                loop = target // 10

        except ValueError:
            print("[WARN][{0}] Input Format/Data Error".format(time.strftime("%H:%M:%S", time.localtime())))
            continue

        print("[INFO][{0}] Scheduled Shutdown Enabled".format(time.strftime("%H:%M:%S", time.localtime())))
        print("[INFO][{0}] {1} Loop Set".format(time.strftime("%H:%M:%S", time.localtime()), loop))
