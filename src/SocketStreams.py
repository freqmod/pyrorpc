#   Copyright (C) 2008 Frederik M.J. Vestre

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

from TwoWayBase import *;
import socket;
import sys;

class SocketChannelBase(TwoWayBase,Thread):    
    def __init__(self,service=None,autoconnect=False):
        Thread.__init__(self);
        TwoWayBase.__init__(self, service, autoconnect);
        self.soc=None
        self.connected=False;
    def setSocket(self,soc):
        self.soc=soc;
    def start(self):
        """ Does not catch any socket exceptions"""
        if(not self.connected and not self.soc==None):
            #start time         
            self.connected=True;
            Thread.start(self);
            
    def WriteString(self,str):
        print "Send:"+str
        self.soc.sendall(str)

    def ReadString(self,len):
        print "Read:"+str(len)
        return self.soc.recv(len)
    def run(self):
        try:
            while(self.connected):
                self.priv.recieveMessage(self.fillMessage(Message_pb2.Message()))
        except Exception,e:
            print "Disconnected"+str(e)
    def shutdownImpl(self,closeStreams):
        if(closeStreams):
            self.soc.close()
            
class SocketChannel(SocketChannelBase):
    def __init__(self,host,port,service=None,autoconnect=False):
        SocketChannelBase.__init__(self,service,autoconnect);
        self.host=host;
        self.port=port;
    def start(self):
        """ Does not catch any socket exceptions"""
        if(not self.connected):
            # Create a socket object:
            self.soc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
            # If any operation takes more than 2 seconds, drop to the "except" below
            self.soc.settimeout( 10 )
            # Connect to the host
            self.soc.connect( ( self.host, self.port ) )  
            #start time         
            self.connected=True;
            Thread.start(self);


class SocketServer(Thread):
    def __init__(self,port,service,host='',autoconnect=False):
        Thread.__init__(self);
        self.service=service
        self.port=port;
        self.host=host;
        self.connected=False
    def start(self):
        """ Does not catch any socket exceptions"""
        if(not self.connected):
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.bind((self.host,self.port))
            self.connected=True;
            Thread.start(self);
    def run(self):
        while(self.connected):
            self.soc.listen(1)
            if(not self.connected):
                return
            conn, addr = self.soc.accept()
            bs=SocketChannelBase(self.service);
            bs.setSocket(conn)
            bs.shutdownCallback=self;
            bs.start()
    def __call__(self,closeStreams):
        self.connected=False;
        self.soc.shutdown(socket.SHUT_RDWR)
        self.soc.close()
        
