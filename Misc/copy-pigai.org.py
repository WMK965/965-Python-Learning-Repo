import time
import pynput
import pyperclip

print("请将文稿复制到剪切板内并切换输入法为英文，延时10s")
time.sleep(10)
txt = pyperclip.paste()
pynput.keyboard = pynput.keyboard.Controller()
for i in txt:
    pynput.keyboard.type(i)
    time.sleep(0.015)
print("finish!")
time.sleep(2)