#TempConvert
print("Please type the temperature data you want to transform")
In = input()
'''
eval()函数可对括号中的含变量表达式做运算
0  1  2  3  4  5  6  :正向递增序号
a  b  c  d  e  f  g
-7 -6 -5 -4 -3 -2 -1 :反向递减序号
使用[]获取字符串中一个或多个字符
str[0]获取第一个字 str[0:2]获取前两个字 str[0:-1]字符串去掉末位后输出 str[1:]去首位
str[m:n[:k]]m位至n位，k为步长
str[::-1]倒置字符串
['F', 'f', '℉'] : 列表类型数据
'''
numdata = eval(In[0:-1])
numdata = float(numdata)
'''
print("{:.2f}".format(value))
:.2f表示填充变量取到小数点后两位
{}表示变量填充位置
'''
if In[-1] in ['F', 'f', '℉']:
    numdata = numdata - 32.0
    numdata = numdata / 180.0
    numdata = numdata * 100.0
    Degree = numdata
    print("Degree Celsius : {:.2f}°C".format(Degree))

elif In[-1] in ['C', 'c', '°C']:
    numdata = numdata / 100.0
    numdata = numdata * 180.0
    numdata = numdata + 32.0
    Fahrenheit = numdata
    print("Fahrenheit scale : {:.2f}℉".format(Fahrenheit))

else:
    print("Syntax Error")
'''
import math  # 引入math库

a = float(input())
b = float(input())
c = float(input())
delta = math.pow(b, 2) - 4 * a * c# 计算判别式
if delta >= 0:
    x1 = (-b + math.sqrt(delta)) / (2 * a)
    x2 = (-b - math.sqrt(delta)) / (2 * a) #括号很重要！！！！！！！！！
    print("X1=", round(x1, 2), "  X2=", round(x2, 2))
else:
    print("没有实数解")
'''
'''
import sys
operation = ["+", "-", "*", "/"]
for i in range(3):
    strin = input()
    strin1 = strin.split(operation[i], 2)[0]
    strin2 = strin.split(operation[i], 2)[-1]
    outp = 0
    strin1 = float(strin1)
    strin2 = float(strin2)
    if operation[i] in strin:
        if i == 0:
            outp = strin1 + strin2
        elif i == 1:
            outp = strin1 - strin2
        elif i == 2:
            outp = strin1 * strin2
        elif i == 3:
            outp = strin1 / strin2
    print(round(outp, 2))
'''
'''
import math

inp = input()
inp = float(inp.split(',', 2)[1]) / math.pow(float(inp.split(',', 2)[0]), 2)
limitg = (0, 18.5, 25, 30, 999999999999999)
limitcn = (0, 18.5, 24, 28, 999999999999999)
outp = ('偏瘦', '正常', '偏胖', '肥胖')
for i in range(0, 5):
    if limitg[i] <= float(inp) < limitg[i + 1]:
        outg = outp[i]
    if limitcn[i] <= float(inp) < limitcn[i + 1]:
        outcn = outp[i]

print(\'''BMI数值为:{0}
BMI指标为:国际'{1}',国内'{2}\'\'''.format(round(inp, 2), outg, outcn))
'''
'''
import numpy as np
import matplotlib.pyplot as plt

data = np.arange(0, 1, 0.001)
plt.title("lines")
plt.xlabel('x')
plt.ylabel('y')
plt.xlim((0, 1))
plt.ylim((0, 1))
b = np.arange(0, 1, 0.2)
plt.xticks(b)
plt.yticks([0, 0.5, 1])
plt.plot(data, np.power(data, 2), linewidth=3, color='blue', linestyle='--')
plt.plot(data, np.power(data, 3), linewidth=1, color='green')
plt.legend(['y=x^2', 'y=x^3'])
plt.savefig("jg.png")
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt


def draw(a):
    t = np.linspace(0, 2 * np.pi, 1025)
    y = a * (2 * np.cos(t) - np.cos(2 * t))
    x = a * (2 * np.sin(t) - np.sin(2 * t))
    plt.xlim(-6, 6)
    plt.ylim(-7, 4)
    plt.plot(x, y, linewidth=1, color='red')
    plt.fill_between(x, y, facecolor='yellow', alpha=0.5)


plt.figure(num=1, figsize=(24, 6))
plt.subplot(1, 3, 1)
draw(0.5)
plt.subplot(1, 3, 2)
draw(1)
plt.subplot(1, 3, 3)
draw(2)
plt.show()
plt.savefig('heart.jpg')
'''
'''
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

A1 = np.loadtxt('ex3.csv', dtype=str, delimiter=',')
X = np.array(A1[13][1:])
Y = np.array(A1[0][1:])
plt.pie(X, labels=Y, autopct='%1.1f%%')
plt.title('各科室总就诊人数')
plt.savefig('饼图.png')
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt

data = np.arange(0, 1, 0.001)
plt.title("lines")
plt.xlabel('x')
plt.ylabel('y')
plt.xlim((0, 1))
plt.ylim((0, 1))
b = np.arange(0, 1, 0.2)
plt.xticks(b)
plt.yticks([0, 0.5, 1])
plt.plot(data, np.power(data, 2), linewidth=3, color='blue', linestyle='--')
plt.plot(data, np.power(data, 3), linewidth=1, color='green')
plt.legend(['y=x^2', 'y=x^3'])
plt.savefig("jg.png")
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt


def draw(a):
    t = np.linspace(0, 2 * np.pi, 1025)
    y = a * (2 * np.cos(t) - np.cos(2 * t))
    x = a * (2 * np.sin(t) - np.sin(2 * t))
    plt.xlim(-6, 6)
    plt.ylim(-7, 4)
    plt.plot(x, y, linewidth=1, color='red')
    plt.fill_between(x, y, facecolor='yellow', alpha=0.5)


plt.figure(num=1, figsize=(24, 6))
plt.subplot(1, 3, 1)
draw(0.5)
plt.subplot(1, 3, 2)
draw(1)
plt.subplot(1, 3, 3)
draw(2)
plt.show()
plt.savefig('heart.jpg')
'''
'''
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

A1 = np.loadtxt('ex3.csv', dtype=str, delimiter=',')
X = np.array(A1[13][1:])
Y = np.array(A1[0][1:])
plt.pie(X, labels=Y, autopct='%1.1f%%')
plt.title('各科室总就诊人数')
plt.savefig('饼图.png')
plt.show()
'''