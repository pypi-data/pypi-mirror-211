# Socket Server Tools
Use sockets easily
## Installation
To install the latest version run
Unix/macOS:
```
python3 -m pip install sockettools
```
Windows:
```
py -m pip install sockettools
```
To install a specified release run
Unix/maxOS
```
python3 -m pip install sockettools=[version]
```
Windows:
```
py -m pip install sockettools=[version]
```
## Quickstart
server.py:
```python
import network

class TransferProtocol(network.Protocol):
    @classmethod
    def encode(cls, data):
        # This function gets data that the program wants to send and encodes it to bytearray or bytes to send to socket
        return data
    
    @classmethod
    def decode(cls, data : bytearray):
        # This function is called every tome some data is recieved
        # returns CONTINUE if data should be continued to be recieved and data param is continued to be built up
        # If the function returns data: data param is reset and resu't is returned
        return data

class ClientHandler(network.ClientHandler):
    protocol = TransferProtocol # This protocol only allows sending and recieving binary data
    def __init__(self, conn, addr, server):
        # This function is called it the main thread when a client connects
        # conn - socket object of the client connection
        # addr - client address
        # server - Server which created the client hander
        # You sould call the original init for the handler to work
        super().__init__(conn, addr, server)
    def serve():
        # This function is called in a separate thread after the init
        self.transport.run_background() # Activates events
        self.event.register(self.event.PACKET_RECIEVED, self.on_recieved)
    def on_recieved(self, data):
        self.transport.send(data)

echo_server = network.Server(host="0.0.0.0", port=8085, handler=ClientHandler)
echo_server.run()
```
client.py:
```python
import network
class TransferProtocol(same as in server.py)

class Client(network.Client):
    protocol = TransferProtocol
    # Same as ClientHandler
    def serve():
        ...
        self.transport.send(b"Echo test")
    def on_recieved(self, data):
        print(data)

client = Client.conect("127.0.0.1", 8085)
client.run()
```
