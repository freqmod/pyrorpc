#   Copyright (C) 2008 Frederik M.J. Vestre

#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

from TwoWayBase import *;
 
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


