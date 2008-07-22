from google.protobuf.service import RpcController

class SimpleRpcController(RpcController):
    def __init__(self):
        self.Reset();

    def Reset(self):
        """Resets the RpcController to its initial state.
    
        After the RpcController has been reset, it may be reused in
        a new call. Must not be called while an RPC is in progress.
        """
        self.reason="";
        self.hasFailed=False;
        self.canceled=False;
        self.cancelListeners=set();
        self.controllerInfoListeners=set();

    def Failed(self):
        """Returns true if the call failed.
    
        After a call has finished, returns true if the call failed.  The possible
        reasons for failure depend on the RPC implementation.  Failed() must not
        be called before a call has finished.  If Failed() returns true, the
        contents of the response message are undefined.
        """
        return self.hasFailed;

    def ErrorText(self):
        """If Failed is true, returns a human-readable description of the error."""
        return self.reason

    def StartCancel(self):
        """Initiate cancellation.
    
        Advises the RPC system that the caller desires that the RPC call be
        canceled.  The RPC system may cancel it immediately, may wait awhile and
        then cancel it, or may not even cancel the call at all.  If the call is
        canceled, the "done" callback will still be called and the RpcController
        will indicate that the call failed at that time.
        """
        self.canceled=True
        for lst in self.cancelListeners:
            lst.run(None);
        for lst in self.controllerInfoListeners:
            lst.canceled();

      # Server-side methods below
    
    def SetFailed(self, reason):
        """Sets a failure reason.
    
        Causes Failed() to return true on the client side.  "reason" will be
        incorporated into the message returned by ErrorText().  If you find
        you need to return machine-readable information about failures, you
        should incorporate it into your response protocol buffer and should
        NOT call SetFailed().
        """
        self.hasFailed=True
        self.reason=reason
        for lst in self.controllerInfoListeners:
            lst.failed(reason);

    def IsCanceled(self):
        """Checks if the client cancelled the RPC.
    
        If true, indicates that the client canceled the RPC, so the server may
        as well give up on replying to it.  The server should still call the
        final "done" callback.
        """
        return self.canceled;

    def NotifyOnCancel(self, callback):
        """Adds a callback to invoke on cancel.
    
        Asks that the given callback be called when the RPC is canceled.  The
        callback will always be called exactly once.  If the RPC completes without
        being canceled, the callback will be called after completion.  If the RPC
        has already been canceled when NotifyOnCancel() is called, the callback
        will be called immediately.
    
        NotifyOnCancel() must be called no more than once per request.
        """
        self.cancelListeners.add(callback);
    def RemoveNotifyOnCancel(self,callback):
        self.cancelListeners.discard(callback);
    def AddControllerInfoListener(self,lst):
        self.controllerInfoListeners.add(lst);
    def RemoveControllerInfoListener(self,lst):
        self.controllerInfoListeners.discard(lst);
