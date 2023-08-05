#
# 2011.11.17 created
# 2011.11.30 delete test print
# 2014. 5.20 add flush_io() in _tkQ_cb()
# 2019.11.20 define apply and import queue for python3
#
import ca
from ca import *

try :
    apply
except NameError :
    exec('def apply(f,a,k={}) : return f(*a,**k)')

_Queue = None
DEFAULT_INTERVAL = 0.0  # 0.0 means no repeat
_tkQ_state = 0
_tkQ_id = ''
tkQ_INTERVAL = 0.2

def initQ(qmode=None) :
    global _Queue,Queue
    if qmode is None :
        if hasattr(ca,'revision') : qmode = 1
        else                      : qmode = 0
    if qmode :
        try :
            import Queue
        except ImportError :
            import queue
            Queue = queue
        _Queue = Queue.Queue(0)

def _Qput(cb,*args) :
    _Queue.put((cb,args))

def evalQ(n=0) :
    if _Queue is None : return
    while 1 :
        try :
            cb,args = _Queue.get_nowait()
        except Queue.Empty :
            break
        apply(cb,args)
        if n>0 :
            n = n-1;
            if n==0 : break

def pend_eventQ(tmo,interval=None) :
    if _Queue is None :
        return ca.pend_event(tmo)
    if interval is None : interval = DEFAULT_INTERVAL
    t = float(tmo)
    dt = float(interval)
    if t==0.0 :    # infinite loop
        if dt<=0.0 : dt = 1.0
        while 1 :
            r = ca.pend_event(dt)
            evalQ()
    elif dt<=0.0 : # no repeat
        r = ca.pend_event(t)
        evalQ()
    else :         # repeat
        while 1 :
            if dt>t : dt = t
            r = ca.pend_event(dt)
            evalQ()
            t = t-dt
            if t<=0 : break
    return r

def _tkQ_cb(widget,ms) :
    global _tkQ_state,_tkQ_id
    if _tkQ_state==0 : return
    evalQ()
    ca.flush_io()
    _tkQ_id = widget.after(ms,_tkQ_cb,widget,ms)

def tkQ(widget,interval=None) :
    if _Queue is None : return None
    global _tkQ_state,_tkQ_id
    if interval is None : interval = tkQ_INTERVAL
    if _tkQ_state!=0 : return None
    _tkQ_state = 1
    ms = int(interval*1000)
    _tkQ_id = widget.after(ms,_tkQ_cb,widget,ms)
    return _tkQ_id

def tkQ_cancel(widget) :
    if _Queue is None : return
    global _tkQ_state,_tkQ_id
    widget.after_cancel(_tkQ_id)
    _tkQ_state = 0

class channel(ca.channel) :
    def __init__(self,name,cb=None,*args,**kw) :
        if _Queue is None :
            apply(ca.channel.__init__, (self, name, cb)+args, kw)
            return
        if not cb : cb=self.update_info
        apply(ca.channel.__init__, (self, name, lambda c=cb:_Qput(c))+args, kw)
    get0 = ca.channel.get
    put0 = ca.channel.put
    put_and_notify0 = ca.channel.put_and_notify
    monitor0 = ca.channel.monitor
    def get(self,cb=None,*args,**kw) :
        if _Queue is None :
            return apply(ca.channel.get, (self,cb)+args, kw)
        if not cb : cb = self.update_val
        return apply(ca.channel.get,
                     (self, lambda x,c=cb:_Qput(c,x) )+args, kw)
    def put(self,*val,**kw) :
        if _Queue is not None :
            cb = kw.get('cb')
            if cb is not None :
                kw['cb'] = lambda x,c=cb:_Qput(c,x)
        return apply(ca.channel.put, (self,)+val, kw)
    put_and_notify = put
    def monitor(self,callback=None,*args,**kw) :
        if _Queue is None :
            return apply(ca.channel.monitor, (self,callback)+args, kw)
        if not callback : raise ca.PyCa_NoCallback
        return apply(ca.channel.monitor,
                     (self, lambda x,c=callback:_Qput(c,x) )+args, kw)
