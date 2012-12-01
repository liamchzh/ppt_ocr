# -*- encoding:utf-8 -*-

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox as box
import tkFileDialog
import ImageFilter

def load_image(): 
    global im
    global name
    name = tkFileDialog.askopenfilename(initialdir = 'E:/Python')
    if name != '':
        if is_image(name):
            im = Image.open(name)
            im = im.resize((600, 400))
            show_pri_image(im)
        else:
            box.showerror("ERROR", "please choose a image file")
    else:
        box.showerror("ERROR", "please choose a file")
    
def is_image(filename):
    im = Image.open(filename)
    if im.format == 'JPEG' or im.format == 'TIFF':
        return 1
    else:
        return 0

def show_pri_image(im):
    img = ImageTk.PhotoImage(im)
    im_label1.configure(image = img)
    im_label1.image = img

def show_image(im):
    img = ImageTk.PhotoImage(im)
    im_label2.configure(image = img)
    im_label2.image = img

def auto_cut():
    nim = im.convert('L')
    show_image(nim)
    w,h = im.size
    nim_pix = nim.load()
    find(w, h, nim_pix)
    #up, down, left, right = find(w, h, nim_pix)
    #box = (left, up, right, down)
    #new_im = im.crop(box)
    #show(new_im) 
    
def find(w, h, nim_pix):
    up = 0
    down = 0
    left = 0
    right = 0
    row = []
    column = []
    for i in range(w):
        sum = 0
        for j in range(h):
            sum += nim_pix[i, j]
        row.append(sum/w)
    for i in range(h):
        sum = 0
        for j in range(w):
            sum += nim_pix[j, i]
        column.append(sum/h)
    print column
    thres = 50
    up, down = fun(thres, row)
    left, right = fun(thres, column)
    print up, down, left, right

def fun(thres, list):
    a = []
    for i in range(len(list)):
        if list[i] > thres:
            a.append(i)
    print a
    return min(a), max(a)

def cut(up, down, left, right):
    pass



def main():
    root = Tk()
    root.title("PPT_Character Recognition")
    root.geometry("1350x650+0+0")
    
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff = 0)
    filemenu.add_command(label = 'Open', command = lambda:load_image())
##    filemenu.add_command(label = 'Save', command = lambda:save())
    menubar.add_cascade(label= 'File', menu = filemenu)
    root.config(menu = menubar)
    
    global im_label1
    global im_label2
    emp_img = ImageTk.PhotoImage(Image.new('L',(1,1)))
    im_label1 = Label(root, image = emp_img, width = 600, height = 400, justify = 'left')
    im_label1.grid(row = 0, column = 0)
    im_label2 = Label(root, image = emp_img, width = 600, height = 400, justify = 'right')
    im_label2.grid(row = 0, column = 1)
    l = StringVar()
    u = StringVar()
    r = StringVar()
    d = StringVar()
    #left = Entry(root, textvariable = l, width = 10)
    #left.grid(row = 1, column = 0)
    up = Entry(root, textvariable = u, width = 10)
    up.grid(row = 1, column = 1)
    right = Entry(root, textvariable = r, width = 10)
    right.grid(row = 1, column = 2)
    down = Entry(root, textvariable = d, width = 10)
    down.grid(row = 1, column = 3)

    btn1 = Button(text=u'自动裁剪', command = auto_cut)
    btn1.grid(row = 1, column = 0)
    root.mainloop()

if __name__ == '__main__':
    main()
