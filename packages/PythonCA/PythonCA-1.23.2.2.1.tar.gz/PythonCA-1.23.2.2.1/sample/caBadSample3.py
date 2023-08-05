#!python
#-*- coding:utf-8 -*-
from __future__ import print_function
import ca
import time,_thread


def cb(self, valstat) :
    print("%08x"%_thread.get_ident(), time.time(),self.name, valstat)


jane = ca.channel('jane')
janet = ca.channel('janet')
fred =ca.channel("fred")
freddy =ca.channel("freddy")

ca.channel.myCB=cb

janet.wait_conn()

jane.monitor(jane.myCB)
janet.monitor(janet.myCB)
fred.monitor(fred.myCB)
freddy.monitor(freddy.myCB)

ca.flush_io()

import time
def foo():
    global lck
    while 1:
        lck.acquire()
        print("%08x"%_thread.get_ident(),time.time())
        time.sleep(100e-6)
        lck.release()

lck=_thread.allocate_lock()
lck.acquire()

_thread.start_new_thread(foo,())

lck.release()
while 1:
    if(lck.acquire()):
        time.sleep(100e-6)
        lck.release()
