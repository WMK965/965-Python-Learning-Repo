print("1024 * 768 = " + str(1024*768) )
print(r'')
'''
转义字符\可以转义很多字符，比如\n表示换行，\t表示制表符，字符\本身也要转义，所以\\表示的字符就是\
如果字符串里面有很多字符都需要转义，就需要加很多\，为了简化，Python还允许用r''表示''内部的字符串默认不转义
如果字符串内部有很多换行，用\n写在一行里不好阅读，为了简化，Python允许用''''''的格式表示多行内容
'''
r = (85 - 72) / 72 * 100
print(f'{r:.1f}%')
'''
s = input("")  # 输入一个字符串
ls = []
for c in s:
    ls.append(str(ord(str(c))))
print(','.join(ls))
'''
'''
s = \'''双儿 洪七公 赵敏 赵敏 逍遥子 鳌拜 殷天正 金轮法王 乔峰 杨过 洪七公 郭靖 
       杨逍 鳌拜 殷天正 段誉 杨逍 慕容复 阿紫 慕容复 郭芙 乔峰 令狐冲 郭芙 
       金轮法王 小龙女 杨过 慕容复 梅超风 李莫愁 洪七公 张无忌 梅超风 杨逍 
       鳌拜 岳不群 黄药师 黄蓉 段誉 金轮法王 忽必烈 忽必烈 张三丰 乔峰 乔峰 
       阿紫 乔峰 金轮法王 袁冠南 张无忌 郭襄 黄蓉 李莫愁 赵敏 赵敏 郭芙 张三丰 
       乔峰 赵敏 梅超风 双儿 鳌拜 陈家洛 袁冠南 郭芙 郭芙 杨逍 赵敏 金轮法王 
       忽必烈 慕容复 张三丰 赵敏 杨逍 令狐冲 黄药师 袁冠南 杨逍 完颜洪烈 殷天正 
       李莫愁 阿紫 逍遥子 乔峰 逍遥子 完颜洪烈 郭芙 杨逍 张无忌 杨过 慕容复 
       逍遥子 虚竹 双儿 乔峰 郭芙 黄蓉 李莫愁 陈家洛 杨过 忽必烈 鳌拜 王语嫣 
       洪七公 韦小宝 阿朱 梅超风 段誉 岳灵珊 完颜洪烈 乔峰 段誉 杨过 杨过 慕容复 
       黄蓉 杨过 阿紫 杨逍 张三丰 张三丰 赵敏 张三丰 杨逍 黄蓉 金轮法王 郭襄 
       张三丰 令狐冲 赵敏 郭芙 韦小宝 黄药师 阿紫 韦小宝 金轮法王 杨逍 令狐冲 阿紫
       洪七公 袁冠南 双儿 郭靖 鳌拜 谢逊 阿紫 郭襄 梅超风 张无忌 段誉 忽必烈 
       完颜洪烈 双儿 逍遥子 谢逊 完颜洪烈 殷天正 金轮法王 张三丰 双儿 郭襄 阿朱 
       郭襄 双儿 李莫愁 郭襄 忽必烈 金轮法王 张无忌 鳌拜 忽必烈 郭襄 令狐冲 
       谢逊 梅超风 殷天正 段誉 袁冠南 张三丰 王语嫣 阿紫 谢逊 杨过 郭靖 黄蓉 
       双儿 灭绝师太 段誉 张无忌 陈家洛 黄蓉 鳌拜 黄药师 逍遥子 忽必烈 赵敏 
       逍遥子 完颜洪烈 金轮法王 双儿 鳌拜 洪七公 郭芙 郭襄 赵敏''\'
d = {}
count = 0
for i in s.split():
    if i in d:
        d[i] += 1
    else:
        d[i] = 1
print(max(d, key=d.get))'''
'''
import numpy as np

L = [[2.73351472, 0.47539713, 3.63280356, 1.4787706, 3.13661701],
     [1.40305914, 2.27134829, 2.73437132, 1.88939679, 0.0384238],
     [1.56666697, -0.40088431, 0.54893762, 3.3776724, 2.27490386]]
arr = np.array(L)
arr1 = np.array((arr[0][1], arr[1][1], arr[2][1]))
arr1 = arr1.reshape(3, 1)
arr2 = np.array((arr[1][2:5], arr[2][2:5]))
arr3 = np.array((arr[0][1:5:2], arr[2][1:5:2])).flatten()
arr4 = arr[np.where(np.logical_and(arr >= 2.5, arr <= 3.5))]
arr5 = arr[np.where(np.logical_or(arr >= 3, arr <= 0))]
print(f\'''arr1= {arr1}
arr2= {arr2}
arr3= {arr3.flatten()}
arr4= {arr4}
arr5= {arr5}\''')
'''
'''
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

A1 = np.loadtxt('./resources/ex3.csv', dtype=str, delimiter=',')
month = np.array(A1[:, 0][1:13])
n1_data = [eval(x) for x in A1[:, 1][1:13]]
n2_data = [eval(x) for x in A1[:, 2][1:13]]
plt.title('内一科和内二科全年门诊量比较')
plt.xlabel('月份')
plt.ylabel('就诊人数')
plt.plot(month, n1_data, marker='*', color='red', linestyle='-', label='内一科')
plt.plot(month, n2_data, marker='o', color='blue', linestyle='--', label='内二科')
plt.legend(['内一科', '内二科'])
plt.show()
'''
'''
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

A1 = np.loadtxt('ex3.csv', dtype=str, delimiter=',')
month = np.array(A1[:, 0][1:13])
n1_data = [eval(x) for x in A1[:, 1][1:13]]
n2_data = [eval(x) for x in A1[:, 2][1:13]]
plt.title('内一科和内二科全年门诊量比较')
plt.xlabel('月份')
plt.ylabel('就诊人数')
plt.plot(month, n1_data, marker='*', color='red', linestyle='-', label='内一科')
plt.plot(month, n2_data, marker='o', color='blue', linestyle='--', label='内二科')
plt.legend(['内一科', '内二科'])
plt.show()
'''
