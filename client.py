import socket

ADRS = 'localhost'
# ADRS = '10.6.83.153'
PORT = 10000
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"
data = ""  			#string
data = "".encode()	#bytes
data = b"" 			#bytes

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ADRS, PORT))
for byte in data:
    s.send(byte)
data = s.recv(BUFFER_SIZE)
print("received data:", data)
s.close()

