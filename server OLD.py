# -*- coding: utf-8 -*-
# filename          : server.py
# description       : Easily download stuff onto a server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 12-01-2020
# version           : v1.1
# usage             : python main.py
# notes             : 
# license           : MIT
# py version        : 3.7.8 (must run on 3.6 or higher)
#==============================================================================
from __future__ import print_function
import socket

# unused ports: 26490-26999
port = 26490
address = socket.gethostbyname(socket.gethostname())

# IPv4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Binding socket...")
s.bind((address, port))
print(f"Listnening for connections on \'{address}:{port}\"...")
s.listen(5)

def send(msg, encoding="utf8"):
	if msg.replace(" ","") == "":
		print("No text entered, nothing was sent.")
	else:
		clientsocket.send(msg.encode(encoding))
		print(f"Sent URL:\n> {msg}")

clientsocket, address = s.accept()
print(f"Connection from {address} has been established!")
send("Welcome to the server!")

running = True
while running:
	send(input("Enter a URL to send:\n> "))
