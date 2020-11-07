import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.sendto(b"123456789",('127.0.0.1',50000))
sock.close()
