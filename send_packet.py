#!/usr/bin/python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
sock.sendto(b"123456789",('192.168.4.10',50000))
sock.close()
