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
import config as cfg

address = cfg.remote_server_address
port = cfg.server_port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((address, port))
print(s.recv(cfg.network_buffer).decode("utf8"))
while True:
	s.send(input(f"{os.getcwd()}> ").encode("utf8"))
