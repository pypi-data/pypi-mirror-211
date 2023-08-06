import queue as _queue
import threading as _threading
from .events import _events
from .protocol import CONTINUE

class _transport:
    def __init__(self, handler) -> None:
        self.handler = handler
        self.ingoing = _queue.Queue()
        self.outgoing = _queue.Queue()
    
    def run_background(self):
        def input():
            while True:
                message = self.read()
                self.ingoing.put(message)
                self.handler.event._fire(_events.PACKET_RECIEVED, message)
        def output():
            while True:
                message = self.outgoing.get()
                self.send(message)
        input_thread = _threading.Thread(target=input)
        output_thread = _threading.Thread(target=output)

        input_thread.start()
        output_thread.start()

        return input_thread, output_thread

    def read(self, buffer_size = 1):
        connection = self.handler.conn
        protocol = self.handler.protocol
        
        read = bytearray()
        while True:
            buffer = connection.recv(buffer_size)
            for byte in list(buffer):
                read.append(byte)
            decoded = protocol.decode(read)
            if decoded != CONTINUE:
                break
        return decoded

    def send(self, data):
        connection = self.handler.conn
        protocol = self.handler.protocol

        encoded = protocol.encode(data)
        connection.sendall(encoded)
    
    def close(self):
        self.handler.conn.close()