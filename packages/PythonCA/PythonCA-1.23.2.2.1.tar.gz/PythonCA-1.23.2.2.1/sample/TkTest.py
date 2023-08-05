#!python
#-*- coding:utf-8 -*-
from __future__ import print_function
from  tkinter import *

f=LabelFrame(text="label")
f.pack()
v=IntVar()
e=Entry(f, textvariable=v)
def cb():
    global v,e
    v.set(v.get()+1)

def bg(cb):
    cb()
    e.after_idle(bg,cb)

e.pack()
e.after(1000,bg,cb)
e.mainloop()
