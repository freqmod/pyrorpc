# -*- coding: utf-8 -*-
#   Copyright (C) 2008 Frederik M.J. Vestre

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

from threading import *;

class ResponseWaiter:
    def __init__(self,bch, ctrl):
        self.priv=ResponseWaiter.ResponseWaiterPrivate(self);
        self.bc=None
        self.co=None

        self._Listen(bch, ctrl);
        self.al=Lock();
        self.wl=Lock();
        self.wc=Condition(self.wl);
        self.responded=False;
        self.cbr=None
        
    def Await(self,timeout=0):
        if (self.responded or ((not self.bc==None) and self.bc.connected==False)):
            return self.cbr;
        self.wl.acquire();
        self.al.acquire();
        try:
            if (timeout == 0):
                self.wc.wait(None);
            else:
                self.wc.wait(timeout);
            if (self.responded):
                return self.cbr;
            else:
                raise Exception("The response timed out");
        finally:
            self.wl.release();
            self.al.release();

    def reset(self,newchan,newco):
        if (self.al.acquire(0)):
            try:
                self.cbr = None;
                self.responded = False;
                self.cleanup();
                self._Listen(newchan,newco);
            finally:
                self.al.release();
        else:
            raise Exception("The response is allready waiting on something");

    #
    # Clean up the waiter after use and remove the pointer to the channel
    #
    def cleanup(self):
        if (not self.bc == None):
            self.bc.RemoveChannelBrokenListener(self.priv);
        if (not self.co == None):
            self.bc.RemoveChannelBrokenListener(self.priv);

    def _Listen(self,bc,co):
        if (not bc == None):
            self.bc=bc;
            self.bc.AddChannelBrokenListener(self.priv);

        if (not co == None):
            self.co=co;
            self.co.AddControllerInfoListener(self.priv);
    def Callback(self):
        return self.priv;

    class ResponseWaiterPrivate:
        def __init__(self,encloser):
            self.encloser=encloser;
        def ChannelBroken(self,b):

            self.encloser.wl.acquire();
            try:
                self.cbr = null;
                self.responded = true;
                self.encloser.wc.NotifyAll();
            finally:
                self.encloser.wl.release();

        def __call__(self,param):
            self.encloser.wl.acquire();
            try:
                self.encloser.cbr = param;
                self.encloser.responded = True;
                self.encloser.wc.notifyAll();
            finally:
                self.encloser.wl.release();
        def canceled(self):
            self.encloser.wl.acquire();
            try:
                self.encloser.cbr = None;
                self.encloser.responded = True;
                self.encloser.wc.notifyAll();
            finally:
                self.encloser.wl.release();

        def failed(self,reason):
            self.encloser.wl.acquire();
            try:
                self.encloser.cbr = None;
                self.encloser.responded = True;
                self.encloser.wc.notifyAll();
            finally:
                self.encloser.wc.release();
