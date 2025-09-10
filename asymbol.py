import tkinter
root = tkinter.Tk()
root.title("")
Canvas = tkinter.Canvas(root, width=500, height=500, bg="red")
Canvas.pack()

Canvas.create_oval(10, 490, 450, 50, fill="white", outline="black", width=2)

Canvas.create_line(340,  120, 159, 160, fill="black", width=45,)
Canvas.create_line( 175, 160,213, 280, fill="black", width=45,)
Canvas.create_line( 213, 280 ,257,420, fill="black", width=45,)
Canvas.create_line( 213, 280 ,360,250, fill="black", width=45,)
Canvas.create_line( 350,240,390, 380, fill="black", width=45,)
Canvas.create_line( 213, 280 ,80,310, fill="black", width=45,)
Canvas.create_line(100,310,50, 170 ,fill="black", width=45,)
Canvas.create_line(267,410,120,440 ,fill="black", width=45,)
root.mainloop()