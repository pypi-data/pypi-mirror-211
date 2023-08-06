from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

def TextBox(text):
    root = Tk()
    img= ImageTk.PhotoImage(Image.open("pylogo.png"))
    root.geometry("300x150")
    t = Label(root, text = text, font = ("lucida", 20))
    t.pack()
    root.title("Python")
    td = Label(root, image = img)

    td.pack(side=RIGHT)

    def Stop():
        root.destroy()

    ok = Button(root, text = "OK", command = Stop)
    ok.place(x = "50", y = "75")
    root.mainloop()

def StringInput(text):
    g = ""   # initialize g


    root = Tk()
    root.title("Python")

    root.geometry("375x150")
    img= ImageTk.PhotoImage(Image.open("pylogo.png"))
    td = Label(root, image = img)
    td.place(x = "180", y = 60)
    #td.pack(side = RIGHT)
    t = Label(root, text = text, font = ("lucida", 20))
    t.place(x = 0, y =15 )
    e = Entry(root, borderwidth = 5, width = 25)
    e.pack(side = LEFT)
    def Stop():
        # declare g as nonlocal variable
        nonlocal g
        # get the value of the entry box before destroying window
        g = e.get()
        root.destroy()
    ok = Button(root, text = "  OK  ", command = Stop)
    ok.place(x = 0, y = 110)
    no = Button(root, text = "Cancel", command = Stop)
    no.place(x = 75, y = 110)
    root.mainloop()

    # return the value of the entry box
    return g
#t = ButtonBox("f")
#print(t)
def Message(fatal, text):

    root = Tk()
    root.geometry("300x150")
    root.withdraw()
    root.title("Python")

    if fatal == True:
        messagebox.showwarning(text, text)

    elif fatal == False:
        messagebox.showinfo(text, text)
    root.destroy()
    root.mainloop()



def IntInput(text):
    g = ""   # initialize g
    g = int()


    root = Tk()
    root.geometry("375x150")
    root.title("Python")

    img= ImageTk.PhotoImage(Image.open("pylogo.png"))
    td = Label(root, image = img)
    td.place(x = "180", y = "5")
    #td.pack(side = RIGHT)
    t = Label(root, text = text, font = ("lucida", 20))
    t.place(x = 0, y =15 )
    e = Entry(root, borderwidth = 5, width = 25)
    e.pack(side = LEFT)
    def Stop():
        # declare g as nonlocal variable
        nonlocal g
        g = int()
        # get the value of the entry box before destroying window
        g = e.get()
        g = int()

        root.destroy()
    ok = Button(root, text = "  OK  ", command = Stop)
    ok.place(x = 0, y = 110)
    no = Button(root, text = "Cancel", command = Stop)
    no.place(x = 75, y = 110)
    root.mainloop()

    # return the value of the entry box
    return g
def DropDown(text, optionone, optiontwo, optionthree):
    g = ""
    root = Tk()
    img= ImageTk.PhotoImage(Image.open("pylogo.png"))
    td = Label(root, image = img)
    root.title("Python")

    td.place(x = "130", y = "-15")
    clicked = StringVar()
    root.geometry("300x150")
    t = Label(root, text = text, font = ("lucida", 20))
    t.place(x = 0, y =15 )
    e = OptionMenu(root, clicked, optionone, optiontwo, optionthree)
    e.place(x = 70, y = 80)
    clicked.set(optionone)

    def Stop():
        nonlocal g
        g = clicked.get()
        root.destroy()
    ok = Button(root, text = "  OK  ", command = Stop)
    ok.place(x = 0, y = 110)
    no = Button(root, text = "Cancel", command = Stop)
    no.place(x = 75, y = 110)
    root.mainloop()
    root.mainloop()
    return g
def YesOrNo(text):
    g = ""
    root = Tk()
    root.geometry("300x150")
    t = Label(root, text = text, font = ("Times New Roman", 20))
    t.place(x = 0, y =0 )
    img= ImageTk.PhotoImage(Image.open("pylogo.png"))
    td = Label(root, image = img)
    td.place(x = "130", y = "-15")
    t.tkraise(td)
    root.title("Python")

    def Stop():
        nonlocal g
        root.destroy()
        g = True
    def Stopa():
        nonlocal g
        root.destroy()
        g = False
    ok = Button(root, text = "  OK  ", command = Stop)
    ok.place(x = 0, y = 110)
    no = Button(root, text = "Cancel", command = Stopa)
    no.place(x = 75, y = 110)
    root.mainloop()
    root.mainloop()

    return g
