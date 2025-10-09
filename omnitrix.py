from turtle import *
from colorsys import *
tracer(100)
speed(90)
hideturtle()
bgcolor("black")
width(2)
h = 0.01
for i in range(450):
    forward(100)
    left(60)
    forward(100)
    right(120)
    circle(50)
    left(240)
    forward(100)
    left(60)
    forward(100)
    color(hsv_to_rgb(h,1,1))
    forward(100)
    right(60)
    forward(100)
    left(120)
    circle(-50)
    right(240)
    forward(100)
    right(60)
    forward(100)
    left(2)
    h += 0.005

done()
