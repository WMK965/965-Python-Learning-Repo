print("")
'''
class Car:
    madeby = '中国'

    def __init__(self, brand, color):  # 1 定义构造方法
        self.brand = brand  # 2 给实例变量 brand 赋值
        self.color = color  # 3 给实例变量 color 赋值

    def stat(self):
        print('{}品牌的{}汽车'.format(self.brand, self.color))  # 4 显示实例变量brand，color

    def run(self):
        self.stat()  # 5 引用stat方法
        print("汽车准许在{}境内行驶".format(self.madeby))  # 6 显示类变量 madeby


bmw = Car("华晨宝马", "火焰蓝色")  # 7 创建对象bmw，华晨宝马,火焰蓝色
benz = Car("奔驰", "银灰色")  # 8 创建对象benz，奔驰,银灰色
Car.madeby = '美国'
bmw.run()
print("{}的{}汽车由{}制造".format(bmw.color, bmw.brand, Car.madeby))  # 9 显示实例变量 color , brand, madeby
benz.color = '雪山白色'  # 10 重置benz对象的color属性为'雪山白色'
benz.stat()
'''
'''
class Doctor:  #1 定义类
    hospital = '广东医附院'  #2 类变量定义
    salary = 8000    
    def __init__(self,name,salary):
        self.name = name  # 实例变量定义 name 
        self.salary = salary  # 实例变量定义 salary
    
    def chkIn(self):  #4 方法名chkIn定义
        print("上班打卡已完成")  # 显示"上班打卡已完成"
    
    def getSalary(self):
        self.chkIn()    
        print("{}医生{}本月的工资是{}元".format(Doctor.hospital,self.name,self.salary))
name=input()        
surgeon=Doctor(name,10000)  # 外科医生
print(Doctor.salary , surgeon.salary )
surgeon.getSalary()
'''