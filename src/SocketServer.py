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
from SocketStreams import *;
from SimpleRpcController import *;
import Exprintconfig_pb2;
import socket
import sys
from inspect import *


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

srv=SocketServer(1246,Exprintservice("rsv",False))
srv.start()

