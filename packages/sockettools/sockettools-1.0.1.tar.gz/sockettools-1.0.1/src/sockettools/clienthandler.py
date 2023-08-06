import socket as _socket
from dataclasses import dataclass as _dataclass
import threading as _threading
from .protocol import Protocol
from .transport import _transport
from .events import _events

class ClientHandler:
    protocol : Protocol = Protocol
    def __init__(self, conn : _socket.socket, addr, server):
        self.conn = conn
        self.addr = addr
        self.server = server
        self.protocol = type(self).protocol
        self.transport = _transport(self)
        events_pre = object.__new__(_events)
        _events.__init__(events_pre, self)
        self.event = events_pre
    
    def serve(self): ...

@_dataclass
class _active_handler:
    handler : ClientHandler
    thread : _threading.Thread