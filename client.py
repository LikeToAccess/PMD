# -*- coding: utf-8 -*-
# filename          : client.py
# description       : Easily download movies onto a server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 04-14-2021
# version           : v1.0
# usage             : python client.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import socket
import os


address = "10.200.10.200"  # server address
port = 26490
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
print(s.recv(1024).decode("utf8"))
while True:
	s.send(input(f"{os.getcwd()}> ").encode("utf8"))
