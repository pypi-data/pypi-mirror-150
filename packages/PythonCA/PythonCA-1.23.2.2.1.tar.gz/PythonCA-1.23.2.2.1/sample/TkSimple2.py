#!/bin/env python
from __future__ import print_function
import _thread
import ca
#import fakeca as ca
from caAlarmSeverity import *
import gc

from tkinter import *
import types,time,_thread

class LabeledEntry(Label):
    def __init__(self, parent, text, *args, **env):
        self.frame=Frame(parent)
        self.label=Label(self.frame,text=text)
        self.label.pack(side=LEFT,fill=X)
        Label.__init__(self, self.frame, *args,**env)
        Label.configure(self, relief=SUNKEN)
        Label.pack(self, side=LEFT,fill=X,expand=True)

    def pack(self, *args,**env):
        self.frame.pack(*args,**env)

    def replace(self,str):
        self.delete(0,len(self.get()))
        self.insert(0,str)

class CaInfoWidget(LabelFrame):
    def init_ca(self, ch):
        if( type(ch) in (str,)):
            self.ch=ca.channel(ch)
            self.ch.wait_conn()
        elif isinstance(ch, ca.channel):
            self.ch=ch
        else:
            raise "No Channel object  nor Channel name"
            
    def __init__(self, parent, ch, *args,**env):
        self.init_ca(ch)
        LabelFrame.__init__(self, parent, text=self.ch.name, *args,**env);
        self.var=StringVar()
        self.varEntry=LabeledEntry(self,   "Value:")#,textvariable=self.var)
        self.varEntry.pack(side=TOP,fill=X)

    def Update(self):
        if self.ch.val:
            self.varEntry.configure(text="%20.7f"%self.ch.val)

    def start_monitor(self):
        self.ca_update_lock=_thread.allocate()
        self.active=True
        self.ch.monitor(callback=self.ca_callback)
        _thread.start_new_thread(self.tk_callback,())
        self.ch.flush()

    def clear_monitor(self):
        self.active=False
        self.ch.clear_monitor()
        self.ch.flush()
        del self.ca_update_lock
            
    def ca_callback(self,vals):
        self.ch.update_val(vals)
        self.ca_update_lock.release()
        
    def tk_callback(self):
        while self.active:
            self.ca_update_lock.acquire()
            self.Update()
        _thread.exit_thread()
        
def test():
    tk=Tk()
    c1=CaInfoWidget(tk, "jane")
    c1.pack()

    c2=CaInfoWidget(tk, "janet")
    c2.pack()
    c1.start_monitor()
    c2.start_monitor()    
    c1.mainloop()

if __name__ =="__main__":
    test()
