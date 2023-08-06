import socket as _socket
import threading as _threading
from .protocol import Protocol
from .transport import _transport
from .events import _events

class Client:
    protocol : Protocol = Protocol

    @classmethod
    def connect(cls, host : str, port : int):
        conn = _socket.socket()
        conn.connect((host, port))
        return cls(conn)

    def __init__(self, conn : _socket.socket = ...):
        self.conn = conn
        self.protocol = type(self).protocol
        self.transport = _transport(self)
        events_pre = object.__new__(_events)
        _events.__init__(events_pre, self)
        self.event = events_pre
        self.stop_event : _threading.Event = None
        self.running_thread : _threading.Thread = None
    
    def serve(self): ...

    def _get_config(self, host = ..., port = ...):
        if self.conn == ... and (host == ... or port == ...):
            raise ValueError("Run requires either config in the constructor or host/port param")
        if self.conn == ...:
            conn = _socket.socket()
            conn.connect((host, port))
        else:
            conn = self.conn
        return conn

    def run(self, host : str = ..., port : int = ...):
        conn = self._get_config(host, port)
        self.conn = conn
        self.serve()

    def start(self, host : str = ..., port : int = ...):
        conn = self._get_config(host, port)
        self.conn = conn

        thread = _threading.Thread(target=self.serve, name="CLIENT_THREAD")
        thread.start()
        self.running_thread = thread
        return thread
    
    def stop(self):
        self.stop_event.set()
        self.running_thread.join()