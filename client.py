import socket

host = "192.168.10.222"
port = 5764
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.close()