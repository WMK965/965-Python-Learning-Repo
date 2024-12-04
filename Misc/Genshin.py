import os
import shutil
import time


def txtreplace(name, path, character, content):
    filename = '{0}\\{1}'.format(path, name)
    txt = open(filename, 'r', encoding='UTF-8')
    lines = txt.readlines()
    savtxt = open(filename, 'w', encoding='UTF-8')
    for i in lines:  # 对TXT 进行逐行读取
        savtxt.write(i.replace(character, content))
    txt.close()
    savtxt.close()


def txtsearch(num, path, character):
    filename = '{0}\\{1}'.format(path, num)
    txt = open(filename, 'r', encoding='UTF-8')
    lines = txt.readlines()
    for lines in lines:  # 对TXT 进行逐行读取
        if character in lines:
            return lines
    txt.close()


dirpath = 'D:\\Genshin Impact Official\\Genshin Impact Game\\'
pluginres = 'D:\\GenshinBiliLoginPlugin\\PCGameSDK.dll'
pluginpath = 'D:\\Genshin Impact Official\\Genshin Impact Game\\YuanShen_Data\\Plugins\\PCGameSDK.dll'
filenam = 'config.ini'
o1 = 'channel=1'
b1 = 'channel=14'
o2 = 'cps=mihoyo'
b2 = 'cps=bilibili'
loop = 1

print('''############################
##\\1切换到官服,2切换到B服/##
############################''')

livedata = str(txtsearch(filenam, dirpath, 'channel='))
ver = 2
if b1 in livedata:
    print('''######\\当前版本： B服/######
############################''')
    ver = 0
elif o1 in livedata:
    print('''######\\当前版本: 官服/######
############################''')
    ver = 1
else:
    print('''############################
####Configuration  Error####
############################''')
des = int(input('输入:'))
while loop < 2:
    if des == 1:
        if ver == 0:
            txtreplace(filenam, dirpath, b1, o1)
            txtreplace(filenam, dirpath, b2, o2)
            os.remove(pluginpath)
            loop = 3
            print('''############################
#########\\Finished/#########
############################''')
        elif ver == 1:
            loop = 3
            print('''############################
####\\已是官服，无需切换/####
############################''')
    elif des == 2:
        if ver == 1:
            txtreplace(filenam, dirpath, o1, b1)
            txtreplace(filenam, dirpath, o2, b2)
            shutil.copyfile(pluginres, pluginpath)
            loop = 3
            print('''############################
#########\\Finished/#########
############################''')
        elif ver == 0:
            loop = 3
            print('''############################
#####\\已是B服,无需切换/#####
############################''')
    else:
        print('''############################
#######\\Input  Error/#######
############################''')
        des = int(input('输入:'))

time.sleep(3)
