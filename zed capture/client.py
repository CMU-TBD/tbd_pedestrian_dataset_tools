import socket

HOST = '172.26.192.189'
PORT = 2111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
data = s.recv(1024)
print('Received: ' + repr(data))
s.close()

print('Machine 2 start working!')
