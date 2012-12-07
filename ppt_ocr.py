# -*- encoding:utf-8 -*-

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox as box
import tkFileDialog
import ImageFilter
from pytesser import *

#载入图像
def load_image(): 
    global im
    global name
    name = tkFileDialog.askopenfilename(initialdir = 'E:/Python')
    if name != '':
        if is_image(name):
            im = Image.open(name)
            im = im.resize((600, 400))
            show_image(im)
        else:
            box.showerror("ERROR", "please choose a image file")
    else:
        box.showerror("ERROR", "please choose a file")
    
#判断是否为jpg or tiff格式
def is_image(filename):
    im = Image.open(filename)
    if im.format == 'JPEG' or im.format == 'TIFF':
        return 1
    else:
        return 0

def yuantu():
    show_image(im)

def show_image(im):
    img = ImageTk.PhotoImage(im)
    im_label1.configure(image = img)
    im_label1.image = img

def auto_cut():
    nim = im.convert('L')
    show_image(nim)
    w,h = im.size
    nim_pix = nim.load()
    up, down, left, right = process(w, h, nim_pix)
    cuted_im = cut(up, down, left, right)
    cuted_im = zengqiang(cuted_im)
    show_image(cuted_im)
    ocr(cuted_im)
    
def ocr(im):
    content = image_to_string(im)
    text_label.configure(text = content)
    text_label.text = content
    
def process(w, h, nim_pix):
    row = []
    column = []
    for i in range(h):
        sum = 0
        for j in range(w):
            sum += nim_pix[j, i]
        row.append(sum/w)
    for i in range(w):
        sum = 0
        for j in range(h):
            sum += nim_pix[i, j]
        column.append(sum/h)
    thres = 50 
    up, down = fun(thres, row)
    left, right =fun(thres, column)
    return up, down, left, right

def fun(thres, list):
    new_list = []
    for item in list:
        if item < thres:
            new_list.append(-80)
        else:
            new_list.append(item)
    return find(new_list)

def find(list):
    sm = 0
    mx = -99999999
    cur = 0
    begin = 0
    end = len(list)-1
    for i in range(len(list)):
        if list[i] > 0:
            begin = i
            break
    while(cur < len(list)):
        sm += list[cur]
        if sm > mx:
            mx = sm
            end = cur
        elif sm < 0:
            sm = 0
        cur += 1
    return begin, end


def cut(up, down, left, right):
    box = (left, up, right, down)
    return im.crop(box)

def zengqiang(im):
    w,h = im.size
    nim = Image.new('L',im.size)
    lim = im.convert('L')
    lpix = lim.load()
    npix = nim.load()
    for i in range(w):
        for j in range(h):
            if lpix[i, j] < 100:
                npix[i, j] = lpix[i, j] * 0.7
            else:
                npix[i, j] = lpix[i, j] * 1.2
    imgfilted = nim.filter(ImageFilter.SHARPEN);
    return imgfilted

def shoudong():
    l = int(lv.get())
    r = int(rv.get())
    u = int(uv.get())
    d = int(dv.get())
    if l < r and u < d and r in range(401) and d in range(601):
        cuted_im = cut(u, d, l, r)
        cuted_im = zengqiang(cuted_im)
        show_image(cuted_im)
        ocr(cuted_im)
    else:
        print u'手动剪裁失败' 

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
    global text_label
    emp_img = ImageTk.PhotoImage(Image.new('L',(1,1)))
    im_label1 = Label(root, image = emp_img, width = 600, height = 400, justify = 'left')
    im_label1.grid(row = 0, column = 0)
    text_label = Label(root, text = 'hi' )
    text_label.grid(row = 0, column = 1)
    global lv, uv, rv, dv
    lv = StringVar()
    uv = StringVar()
    rv = StringVar()
    dv = StringVar()
    
    left = Entry(root, textvariable = lv, text = 'left', width = 10)
    left.grid(row = 3, column = 0)
    up = Entry(root, textvariable = uv, width = 10)
    up.grid(row = 4, column = 0)
    right = Entry(root, textvariable = rv, width = 10)
    right.grid(row = 5, column = 0)
    down = Entry(root, textvariable = dv, width = 10)
    down.grid(row = 6, column = 0)

    btn0 = Button(text=u'显示原图', command = yuantu)
    btn0.grid(row = 1, column = 0)

    btn1 = Button(text=u'自动裁剪', command = auto_cut)
    btn1.grid(row = 2, column = 0)

    btn2 = Button(text=u'手动裁剪', command = shoudong)
    btn2.grid(row = 7, column = 0)
    root.mainloop()
if __name__ == '__main__':
    main()
