
import tkinter 

root = tkinter.Tk()
root.title("my canvas")

Canvas = tkinter.Canvas(root, width=500, height=500, bg="lightblue")
Canvas.pack()

# Add text to the canvas
Canvas.create_text(250, 50, text="Different Shapes Demo", font=("Arial", 18, "bold"), fill="black")

# Rectangle
Canvas.create_rectangle(50, 100, 150, 150, fill="red", outline="darkred", width=3)

# Circle/Oval
Canvas.create_oval(200, 100, 300, 200, fill="green", outline="darkgreen", width=3)

# Triangle (using polygon)
triangle_points = [350, 150, 400, 100, 450, 150]
Canvas.create_polygon(triangle_points, fill="blue", outline="darkblue", width=3)

# Line
Canvas.create_line(50, 200, 200, 250, fill="purple", width=5)

# Arc (partial circle)
Canvas.create_arc(250, 220, 350, 280, start=0, extent=180, fill="orange", outline="darkorange", width=3)

# Star (using polygon)
import math
star_points = []
center_x, center_y = 100, 350
outer_radius = 30
inner_radius = 15
for i in range(10):
    angle = math.pi * i / 5
    if i % 2 == 0:
        radius = outer_radius
    else:
        radius = inner_radius
    x = center_x + radius * math.cos(angle - math.pi/2)
    y = center_y + radius * math.sin(angle - math.pi/2)
    star_points.extend([x, y])
Canvas.create_polygon(star_points, fill="yellow", outline="gold", width=2)

# Rounded rectangle (using multiple shapes)
Canvas.create_arc(300, 300, 320, 320, start=90, extent=90, fill="pink", outline="hotpink", width=2)
Canvas.create_arc(380, 300, 400, 320, start=0, extent=90, fill="pink", outline="hotpink", width=2)
Canvas.create_arc(380, 360, 400, 380, start=270, extent=90, fill="pink", outline="hotpink", width=2)
Canvas.create_arc(300, 360, 320, 380, start=180, extent=90, fill="pink", outline="hotpink", width=2)
Canvas.create_rectangle(310, 300, 390, 380, fill="pink", outline="")
Canvas.create_rectangle(300, 310, 400, 370, fill="pink", outline="")

# Labels for shapes
Canvas.create_text(100, 170, text="Rectangle", font=("Arial", 10), fill="black")
Canvas.create_text(250, 210, text="Circle", font=("Arial", 10), fill="black")
Canvas.create_text(400, 170, text="Triangle", font=("Arial", 10), fill="black")
Canvas.create_text(125, 270, text="Line", font=("Arial", 10), fill="black")
Canvas.create_text(300, 290, text="Arc", font=("Arial", 10), fill="black")
Canvas.create_text(100, 400, text="Star", font=("Arial", 10), fill="black")
Canvas.create_text(350, 400, text="Rounded Rect", font=("Arial", 10), fill="black")

root.mainloop()

