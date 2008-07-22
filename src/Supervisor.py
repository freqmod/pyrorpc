# Copyright (C) 2008 Frederik M.J. Vestre
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY <copyright holder> ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <copyright holder> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from ResponseWaiter import *;
from TwoWayStream import *;
from SimpleRpcController import *;
import Exprintconfig_pb2;
import socket
import sys
from inspect import *

def arrayToString(ary):
        if(ary is None):
            return None
        str=""
        for char in ary:
            str+=char;
        return str
class Filo(object):#also called stack
    def __init__(self):
        self.data = []
    def Puts(self, value):
        self.data.extend(value)
    def Pops(self,ln):
        rt=self.data[ln*-1:]
        self.data=self.data[:ln*-1]
        return rt
class Fifo(object):#also called queue
    def __init__(self):
        self.data = []
    def Puts(self, value):
        self.data.extend(value)
    def Pops(self,ln):
        rt=self.data[:ln]
        self.data=self.data[ln:]
        return rt

class BFifo(object):#also called queue
    def __init__(self):
        self.data = []
        self.cond=Condition()
        self.stopped=False
    def puts(self, value):
        self.data.extend(value)
        self.cond.acquire();
        try:
            #print "Notify"+str(self)
            self.cond.notifyAll();
        finally:
            self.cond.release();
    def pops(self,ln):
        if(self.stopped==True):
            raise IOError("Stream closed")
        ln=int(ln)
        if(len(self.data)<ln):
            while(len(self.data)<ln):
                self.cond.acquire();
                try:
                    #print "Waiting:"+str(len(self.data))+"<"+str(ln)
                    self.cond.wait()
                    if(self.stopped==True):
                        raise IOError("Stream closed")
                finally:
                    self.cond.release()
        #print "Waited"
        rt=self.data[:ln]
        self.data=self.data[ln:]
        return rt
    def stop(self):
        self.stopped=True;
        self.cond.acquire();
        try:
            self.cond.notifyAll();
        finally:
            self.cond.release();
class PipedIOStream(object):
    def __init__(self):
        self.inn=None;
        self.data=BFifo();
    def setInputStream(self,inn):
        self.inn=inn;
    def read(self,len):
        return arrayToString(self.data.pops(len))
    def write(self,data):
        self.inn.put(data);
    def close(self):
        self.data.stop()
    def put(self,data):
        self.data.puts(data)
    def flush(self):
        pass


sinn=PipedIOStream()
sout=PipedIOStream()
cinn=PipedIOStream()
cout=PipedIOStream()
sout.setInputStream(cinn)
cout.setInputStream(sinn);

class Exprintservice(Exprintconfig_pb2.Exprintserver):
#    .Exprintserver implements RpcCallback<Exprintdata.ExprintserverSetConfigResponse>{
    def __init__(self,id,twoway):
        Exprintconfig_pb2.Exprintserver.__init__(self)
        self.id=id;
        self.twoway=twoway;
    def set_config(self,controller,request,done):
        #Handle the request and make a response (se protcol buffers for more info)
        ret=self.id+":"+request.printer;
        for exp in request.exprints:
            ret+="|"+exp.subjectcode+";"+exp.paralell+";"
            if(exp.solutions):
                ret+="jippi"
            else:
                ret+="buu"

        resp=  Exprintconfig_pb2.ExprintserverSetConfigResponse();
        resp.responsecode=ret;
        #Send the response
        done(resp);
        if(self.twoway):
            callBack(controller);#make a call back to the server if configured to do it
    
    def callBack(self,controller):
        #No way to call back witout a TwoWayRpcChannelController to get the RpcChannel back from
        #FIXME: check if it's a twowaycontroller
        twc=controller;
        #Make a response to send back
        cont = SimpleRpcController();
        service = Exprintconfig_pb2.Exprintserver.NewStub(twc.getRpcChannel());#Get the channel back from the TwoWayRpcController
        Exprintconfig_pb2.Exprintconfig.Exprint();
        reqbld.printer="Masmasmas";
        expb =  reqbld.exprints.add();
        expb.paralell="SadHour"
        expb.subjectcode="TMA4140"
        expb.solutions=True;
        #Send a message back
        service.SetConfig(cont, reqbld.build(), this);
    def __call__(self,resp):
        #Handle the response from the message sent back to the server
        print "Got response:"+r.responsecode
    
    def get_config(self,controller,request,done):
        # TODO Auto-generated method stub
        pass;
    
    def reset_config(self,controller,request,done):
        # TODO Auto-generated method stub
        pass;
def servicetest():
    class Tcall:
        def __call__(self,b):
            print b
    exs=Exprintservice("rsv",False)
    met=exs.GetDescriptor().FindMethodByName("set_config");
    ctrl=SimpleRpcController()
    exs.CallMethod(met,ctrl,Exprintconfig_pb2.Exprintconfig(),Tcall())
    print ctrl.ErrorText()
    exit()

srv=TwoWayStream(sinn,sout,Exprintservice("rsv",False))
srv.start()

chan=TwoWayStream(cinn,cout);
chan.start()
#Create a rpc controller to send with the rpc method
cont= SimpleRpcController();
#Create a service that wraps the client channel
service = Exprintconfig_pb2.Exprintserver_Stub(chan);
#Create a responsewaiter that can block while waiting a response from the server
waiter = ResponseWaiter(chan,cont);
#Create and build the message that we send to the method, see the proto buffer documentation for more information
reqbld= Exprintconfig_pb2.Exprintconfig();
reqbld.printer="Morrohjornet"
expb =  reqbld.exprints.add();
expb.paralell="HappyHour";
expb.subjectcode="TFY4125";
expb =  reqbld.exprints.add();
expb.subjectcode="TDT4100"

#Run the RPC method
service.set_config(cont, reqbld,waiter.Callback());
#try:
if(True):
    #Wait for response, if the response is  null, the method is canceled or has failed and the rpc controller will report what happened.
    rpo =waiter.Await();
    #Clean up the waiter, free a pointer to the RpcChannel so it may be garbage collected.
    #Remember to reset the waiter if you want to use it again.
    waiter.cleanup();
    if(rpo is None):
        if(cont.Failed()):
            print "Call failed:"+cont.ErrorText();
        elif(cont.IsCanceled()):
            print "Call canceled";
        else:
            print "Channel broken";
    else:
        #Print out the response code from the response
        print rpo.responsecode
chan.shutdown(True);
#except Exception, inst:
#    print"Error"+str(inst)