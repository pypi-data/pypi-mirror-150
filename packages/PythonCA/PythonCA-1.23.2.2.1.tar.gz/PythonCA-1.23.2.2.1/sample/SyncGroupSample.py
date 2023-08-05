#!/bin/env python3
#-*- coding:utf-8 -*-
from __future__ import print_function

import ca
import time
chs=(
    "fred",
    "freddy",
    "jane",
    "janet",
    # 'alan',
    # 'boot',
    # 'booty',
    # "bill",
    # "billy",
)

import sys,gc

def setup():
    sg=ca.SyncGroup()
    sg.add(chs) # not work in python3
    sg.reset()

    return sg
    
def SyncGroupExample():

    sg=setup()
    sg.GetAll(1.0)
    
    while 1:
        print ("status(before):",sg.test(),time.ctime())
        sg.reset()
        # sg.GetAll(0)
        sg.requestAll()
        print ("status(after):",sg.test(),time.ctime())
        ca.flush()
        sg.wait(2.0)
        if sg.test() == 0:
            sg.convertAll()
            for ch in sg:
                print (ch.name, "\t", ch.val,"\t",
                       ca.TS2Ascii(ch.ts))
            print ("status(Done):",sg.test(),time.ctime())
        ca.pend_event(2.001)
        
if __name__ == "__main__":
    SyncGroupExample()
