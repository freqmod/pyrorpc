# -*- coding: utf-8 -*-
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
from TwoWayStream import *;
import Exprintconfig_pb2;
import socket
import sys
from inspect import *


#sout=open("/home/freqmod/pgmz/protorpcpp/bld/test.in.fifo","w");
#sinn=open("/home/freqmod/pgmz/protorpcpp/bld/test.out.fifo","r");
chan=SocketChannel("localhost",1238);
#chan=TwoWayStream(sinn,sout,None)
chan.start()
print "STSTR"
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
print "2sm"
#Run the RPC method
service.set_config(cont, reqbld,waiter.Callback());
print "snm"
#try:
if(True):
    #Wait for response, if the response is  null, the method is canceled or has failed and the rpc controller will report what happened.
    print "W4A"    
    rpo=None
    try:
      rpo =waiter.Await(3);
    except Exception,e:
      print e
    print "GA"
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
#
print "Finished"
chan.shutdown(True);
#except Exception, inst:
#    print"Error"+str(inst)
