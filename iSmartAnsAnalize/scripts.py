# encoding utf-8
import linecache
import re
import os


def opentxt(num, path, name, line):
    filename = '.\\{0}\\{1}{2}.txt'.format(path, num, name)
    cont = linecache.getline(filename, line)
    return cont


def savetxt(num, path, inv, name, character):
    filename = '.\\{0}\\{1}{2}.txt'.format(path, num, name)
    with open(filename, 'w', encoding='UTF-8') as txt:
        txt.write(inv.replace(character, '\n'))


def txtsearch(num, path, character):
    filename = '.\\{0}\\{1}_Response.txt'.format(path, num)
    txt = open(filename, 'r', encoding='UTF-8')
    lines = txt.readlines()
    for lines in lines:  # 对TXT 进行逐行读取
        if character in lines:
            return lines
    txt.close()


count = 2
while count < 26:
    content = txtsearch(count, 'response', 'answer')
    texts = re.findall(r'<answers>.*<\\/answers>', content)
    texts = str(texts)
    texts = re.findall(r'CDATA\[.]', texts)
    texts = str(texts)
    texts = texts.replace("'CDATA[]]'", '\n')
    texts = texts.replace("CDATA", '')
    savetxt(count, 'Ans', texts, 'ans', ',')
    count += 1

os.chdir(r"C:/Users/965/Builds/iSmartAnsCatch/Ans")
filedir = "C:/Users/965/Builds/iSmartAnsCatch/Ans"
f = open('../Ans.txt', 'w')
# 遍历文件名
for i in range(2, 26):
    filename1 = str(i) + 'ans.txt'
    if i > 0:
        filepath = filedir + '/' + filename1
        # 遍历单个文件 读取行数
        for line1 in open(filepath, encoding='UTF-8'):
            f.writelines(str(i - 1) + line1)
            f.write('\n')
f.close()
