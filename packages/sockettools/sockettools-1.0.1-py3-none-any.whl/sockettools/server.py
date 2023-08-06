import threading as _threading
import random as _random
import socket as _socket
from .clienthandler import ClientHandler, _active_handler
from .events import _events

class Server:
    default_handler : type[ClientHandler] = None
    def __init__(self, host : str = ..., port : int = ..., handler : type[ClientHandler] = ...):
        self.host = host
        self.port = port
        if handler == ...:
            default_handler = type(self).default_handler
            if default_handler == None:
                raise ValueError("Server requires either a default_handler or a handler param")
            else:
                handler = default_handler
        self.handler = handler
        self.handlers: dict[str, _active_handler] = dict()
        self.running_thread : _threading.Thread = None
        self.stop_event = _threading.Event()

    def _get_config(self, host = ..., port = ...):
        if self.host == ... and host == ...:
            raise ValueError("Run requires either config in the constructor or host/port param")
        if self.port == ... and port == ...:
            raise ValueError("Run requires either config in the constructor or host/port param")
        if host == ...:
            host = self.host
        if port == ...:
            port = self.port
        return host, port
    
    def _generate_hid(self, length=10):
        alf = "abcdefghijklmnopqrstuvwxyz"
        alf += alf.upper()
        alf += "1234567890"
        p = ""
        for _ in range(length):
            p += _random.choice(alf)
        return p
    
    def _handle(self, conn, addr, handler, hid):
        try:
            handler.serve()
        except Exception as e:
            handler.event._fire(_events.EXCEPTION, e)
            if handler.event.registered.get(_events.EXCEPTION, []) == []:
                raise

    def _serve_forever(self, host, port, stop_event=None):
        '''Internal. Does not perform prerun check'''
        self.socket = _socket.socket()
        self.socket.bind((host, port))
        self.socket.listen()
        self.socket.setblocking(0)
        while True:
            try:
                connection, addr = self.socket.accept()
                new_handler = self.handler(connection, addr, self)
                while True:
                    handler_id = self._generate_hid()
                    if handler_id not in self.handlers.keys():
                        break
                thread = _threading.Thread(target=self._handle, name=handler_id, args=(connection, addr, new_handler, handler_id))
                self.handlers[handler_id] = _active_handler(new_handler, thread)
                thread.start()
            except BlockingIOError:
                pass
            if stop_event is not None and stop_event.isSet():
                break
    
    def run(self, host : str = ..., port : int = ...):
        '''Runs server in the active thread.'''
        host, port = self._get_config(host, port)
        self._serve_forever(host, port)
    
    def start(self, host : str = ..., port : int = ...):
        '''Runs server in a new thread.'''
        host, port = self._get_config(host, port)

        stop_event = _threading.Event()
        thread = _threading.Thread(target=self._serve_forever, name="SERVER_THREAD", args=(host, port, stop_event), daemon=True)
        thread.start()
        self.stop_event = stop_event
        self.running_thread = thread
        return thread
    
    def stop(self):
        self.stop_event.set()
        self.running_thread.join()