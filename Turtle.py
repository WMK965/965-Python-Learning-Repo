print("")
'''
numlist = "零一二三四五六七八九"
serial = input()
for c in serial:
    print(numlist[eval(c)], end="")
    print(eval(c), end="")
'''
'''
temp = input()
temp = float(temp)
text = "Hello World"
if temp == 0.00:
    print(text)
elif temp < 0.00:
    for c in text:
        print(c)
elif temp > 0.00:
    print("He\nll\no \nWo\nrl\nd")
'''
'''
a = eval(input())
print("{:.2f}".format(a))
'''
'''
import turtle
turtle.setup(1024, 400, 200, 100)
turtle.penup()
turtle.fd(-250)
turtle.pendown()
turtle.pensize(20)
turtle.pencolor("yellow")
turtle.seth(-40)
for i in range(5):
    turtle. circle(40, 80)
    turtle. circle(-40, 80)
turtle.circle(40, 80/2)
turtle.fd(40)
turtle.circle(16, 180)
turtle.fd(40 * 2/3)
turtle.done()
'''
'''
#!/usr/bin/env python
import turtle
turtle.setup(400, 400, 200, 200)
turtle.penup()
turtle.goto(-150, 100)
turtle.pendown()
turtle.pensize(5)
turtle.pencolor("orange")
turtle.seth(0)
for i in range(3):
    turtle.fd(200)
    turtle.rt(120)
turtle.done()
'''
'''
import turtle
circlex = (-220, 0, 220, -110, 110)
circley = (-75, -75, -75, -155, -155)
circlecolor = ("red", "green", "blue", "yellow", "black")
turtle.setup(800, 600, 200, 200)
for i in range(5):
    turtle.pensize(10)
    turtle.pencolor(circlecolor[i])
    turtle.penup()
    turtle.goto(circlex[i], circley[i])
    turtle.pendown()
    turtle.circle(100, 360)
turtle.done()
'''
'''
from turtle import*
width(5)
color = ["red", "blue", "green", "yellow", "black"]
x = [-220, 0, 220, -110, 110]
y = [-75, -75, -75, -155, -155]
for i in range(0, 5):
    penup()
    goto(x[i], y[i])
    color(colour[i])
    pendown()
    circle(100)
'''
'''
import turtle


def circle(x, y, degree, r, width, color):
    turtle.penup()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.width(width)
    turtle.pendown()
    turtle.circle(r, degree)


color = ["red", "blue", "green", "yellow", "black"]
x = [-220, 0, 220, -110, 110]
y = [-75, -75, -75, -155, -155]

for i in range(5):
    circle(x[i], y[i], 360, 100, 15, color[i])
turtle.done()
'''
