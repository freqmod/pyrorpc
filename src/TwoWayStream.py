#   Copyright (C) 2008 Frederik M.J. Vestre

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0


from google.protobuf.service import RpcController
from google.protobuf.service import RpcChannel
from twisted.protocols.basic import Int32StringReceiver
from twisted.internet.defer import Deferred
import Message_pb2
from SimpleRpcController import *;
from struct import *;
from threading import *;
class StreamServerCallback():
    def __init__(self,src,id,ctrl):
        self.src=src;
        self.id=id;
        self.ctrl=ctrl;
    def __call__(self,o):
        self.src.response(self.id,o,self.ctrl);

class TwoWayBase(RpcChannel):
#    protected DataInputStream in;
#    protected DataOutputStream out;
#    private int timeout = 10000;
#    private Service service=null;
#    private boolean connected=false;
#    private Object session=null;
#    private boolean spawnCallers=false;
#    private int protoversion=-1;
#    private HashMap<Integer,Trio<RpcCallback<Message>,RpcController, Message>> currentCalls=new HashMap<Integer, Trio<RpcCallback<Message>,RpcController ,Message>>();
#    private Lock streamlock=new ReentrantLock();
#    private Condition initcond = streamlock.newCondition();
#    private RpcCallback<Boolean> shutdownCallback;
#    private HashSet<ChannelBrokenListener> channelBrokenListeners= new HashSet<ChannelBrokenListener>();
#    HiddenMethods hiddenmethods=new HiddenMethods(this);
#    private RpcController descriptorRequestController=null;
#    private RpcCallback<Pair<String,FileDescriptor>> gotDescriptorCallback=null;
    def __init__(self,service=None,autoconnect=False):
      self.service=service;
      self.callnum=0;
      self.calls=dict();
      self.descriptorRequestController=None;
      self.gotDescriptorCallback=None;
      self.shutdownCallback=None;# FIXME: Make sure there is a way to set shudowncallback
      self.priv= self.PrivateTwoWayBase(self);
      self.connected=False
      if(autoconnect):
        start();
    def start(self):
        pass;
    def CallMethod(self, method, controller, request, response, done):
        req=Message_pb2.Message();
        req.type=Message_pb2.REQUEST;
        req.id=self.callnum;
        req.name=method.name;
        req.buffer=request.SerializeToString();
        self.WriteMessage(req);
        self.calls[self.callnum]=(done,controller,response);
        self.callnum+=1;
    def RequestServiceDescriptor(self,cb,ctrl):
      raise NotImplemented;#supporting methods not implemented 
      if(not (self.descriptorRequestController==None and self.gotDescriptorCallback==None)):
          ctrl.failed="Can't make two descriptor requests at the same time";
          return;
      req=Message_pb2.Message();
      req.type=Message_pb2.REQUEST
      self.WriteMessage(self,req);
      self.descriptorRequestController=ctrl;
      self.gotDescriptorCallback=cb;
      
    def WriteMessage(self,msg):
        str=pack("H",msg.ByteSize())+msg.SerializeToString();
        self.WriteString(str);
    def fillMessage(self,msg):
        len=unpack("H",self.ReadString(2))[0];
        if(len==-1):
            return None
        msgbuf=self.ReadString(len);
        msg.ParseFromString(msgbuf)
        return msg
    #should be implemented by subclass
    #def Start(self):
    #    pass;
    def shutdown(self,closeStreams):
      if(self.connected):
          req=Message_pb2.Message();
          req.type=Message_pb2.DISCONNECT
          self.WriteMessage(req);
          self.shutdownImpl(closeStreams);
          if(not self.shutdownCallback==None):
                self.shutdownCallback.Run(false);
    #protocol buffers for python does not implement the required methods
    def GenerateDescriptorResponse(parent,serviceName):
        raise NotImplemented();
    def ParseDescriptorResponse(parent):
        raise NotImplemented();
    def AddChannelBrokenListener(self,lst):
        self.priv.brokenChannelListeners.add(lst);
    def RemoveChannelBrokenListener(self,lst):
        self.priv.brokenChannelListeners.discard(lst);
    class PrivateTwoWayBase:
        def __init__(self,encloser):
            self.encloser=encloser;
            self.brokenChannelListeners=set();
        def recieveMessage(self,inmsg):
            method=None;
            request=None;
            controller=None;
            if(None is inmsg or inmsg.type==Message_pb2.DISCONNECT):
                connected=False;
                self._shutdownConnection();
            elif(inmsg.type==Message_pb2.REQUEST):
                if(self.encloser.service==None):
                    resp=Message_pb2.Message();
                    resp.type=Message_pb2.RESPONSE_NOT_IMPLEMENTED
                    resp.id=inmsg.id;
                    self.encloser.WriteMessage(resp);
                else:
                    method=self.encloser.service.GetDescriptor().FindMethodByName(inmsg.name)
                    if(method==None):
                        resp=Message_pb2.Message();
                        resp.type=Message_pb2.RESPONSE_NOT_IMPLEMENTED
                        resp.id=inmsg.id;
                        self.encloser.WriteMessage(resp);
                    else:
                        request = self.encloser.service.GetRequestClass(method)()
                        request.ParseFromString(inmsg.buffer)
                        controller = TwoWayRpcController(self.encloser);                      
                        controller.NotifyOnCancel(StreamServerCallback(self, inmsg.id,controller));
                        self.encloser.service.CallMethod(method, controller, request,StreamServerCallback(self,inmsg.id,controller));
            elif(inmsg.type==Message_pb2.DESCRIPTOR_REQUEST):
                resp=Message_pb2.Message();
                resp.type=Message_pb2.DESCRIPTOR_RESPONSE
                self.WriteMessage(resp);
            elif(inmsg.type==Message_pb2.RESPONSE):
                if (inmsg.id in self.encloser.calls):
                    msg = self.encloser.calls[inmsg.id];
                    response = msg[2]();
                    response.ParseFromString(inmsg.buffer);
                    msg[0](response);
                    del self.encloser.calls[inmsg.id];

            elif(inmsg.type==Message_pb2.RESPONSE_CANCEL):
                if (inmsg.id in self.encloser.calls):
                    msg = self.encloser.calls[inmsg.id];
                    msg[1].StartCancel();
                    del self.encloser.calls[inmsg.id];
            elif(inmsg.type==Message_pb2.RESPONSE_FAILED):
                if (inmsg.id in self.encloser.calls):
                    msg = self.encloser.calls[inmsg.id];
                    msg[1].SetFailed(inmsg.buffer);
                    del self.encloser.calls[inmsg.id];
            elif(inmsg.type==Message_pb2.RESPONSE_NOT_IMPLEMENTED):
                if (inmsg.id in self.encloser.calls):
                    msg = self.encloser.calls[inmsg.id];
                    msg[1].SetFailed("Not implemented by peer");
                    del self.encloser.calls[inmsg.id];
            elif(inmsg.type==Message_pb2.DESCRIPTOR_RESPONSE and not (self.encloser.descriptorResponseController==None or self.encloser.getDescriptorCallback==None)):
                self.encloser.descriptorRequestController.setFailed("Service descriptor exploration not supported in python yet");
                self.encloser.gotDescriptorCallback.run(None);
                self.descriptorRequestController=null;
                self.gotDescriptorCallback=null;
        def _shutdownConnection(self):
            connected=False;
            if(not self.encloser.shutdownCallback==None):
                self.encloser.shutdownCallback.Run(false);
            self.fireChannelBroken();
            self.encloser.shutdown(True);#use true here?
        def response(self,id,param,ctrl):
            if (param is None):#canceled or failed
                if(ctrl.Failed()):
                    resp=Message_pb2.Message();
                    resp.type=Message_pb2.RESPONSE_FAILED
                    resp.buffer=ctrl.ErrorText()
                    resp.id=id;
                    self.encloser.WriteMessage(resp);
                else:
                    resp=Message_pb2.Message();
                    resp.type=Message_pb2.RESPONSE_CANCEL
                    resp.id=id;
                    self.encloser.WriteMessage(resp);
            else:
                resp=Message_pb2.Message();
                resp.type=Message_pb2.RESPONSE
                resp.id=id;
                resp.buffer=param.SerializeToString();
                self.encloser.WriteMessage(resp);
        def fireChannelBroken(self):
            for lst in self.brokenChannelListeners: 
                lst.ChannelBroken(self.encloser);
    
class TwoWayStream(TwoWayBase,Thread):
    def __init__(self,inn,out,service=None,autoconnect=False):
        Thread.__init__(self);
        TwoWayBase.__init__(self, service, autoconnect);
        self.inn=inn
        self.out=out
    def start(self):
        if(not self.connected):
            self.connected=True;
            Thread.start(self);
    def WriteString(self,str):
        self.out.write(str);
        self.out.flush();
    def ReadString(self,len):
        return self.inn.read(len);
    def run(self):
        try:
            while(self.connected):
                self.priv.recieveMessage(self.fillMessage(Message_pb2.Message()))
        except IOError, e:
            print e
    def shutdownImpl(self,closeStreams):
        if(closeStreams):
            self.inn.close();
            self.out.close();

class TwoWayRpcController(SimpleRpcController):
    def __init__(self,str):
        SimpleRpcController.__init__(self);
        self.str=str;
    def GetSessionId(self):
        return self.str.GetSessionId();
    def SetSessionId(self,id):
        self.str.SetSessionId(id);
    def getTwoWayBase(self):
        return str;
    def getRpcChannel(self):
        return str;

