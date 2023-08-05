#!python
#-*- coding:utf-8 -*-
from __future__ import print_function
import select
import ca

class SimpleFileManager(dict):
    def __init__(self):
        super(dict, self).__init__()

    def mainloop(self):
        fds=list(self.keys())
        while 1:
            r,w,e=select.select(fds,fds,[],None)
            #print r,w,e
            if r:
                ca.poll()
                
    def do_one_event(self):
        fds=list(self.keys())
        r,w,e=select.select(fds,[],[])
        for f in r:
            ca.poll()

    def loop(self):
        after(fmgr.loop)
        self.do_one_event()

fmgr=SimpleFileManager()

def fd_register(arg, fd, cond):
    print("fd_register",fd, cond, arg)
    if cond:
        fmgr[fd]=arg
    else:
        if fd in fmgr:
            del fmgr[fd]
import ca

def test():
    ca.add_fd_registration(fd_register,0.01)
    ca.Monitor("freddy")
    ca.Monitor("fred")
    ca.Monitor("jane")
    ca.Monitor("janet")
    
    fmgr.mainloop()

if __name__ == "__main__":
    test()
