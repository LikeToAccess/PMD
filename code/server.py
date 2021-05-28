# -*- coding: utf-8 -*-
# filename          : server.py
# description       : Easily download movies onto a server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 04-14-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import socket
import os
from threading import Thread
import download
import config as cfg


def on_new_user(client, address, host=socket.gethostbyname(socket.gethostname())):
	print("Running new instance...")
	client = Client(client, address, host)
	client.run()

def start_bot():
	os.system("python bot.py")


class Client:
		def __init__(self, client, address, host):
			self.host = host
			self.client = client
			self.address = address
			self.buffer = cfg.network_buffer

		def send(self, msg, encoding="utf8"):
			if msg.strip() == "":
				return "Blank message, nothing was sent."
			try:
				self.client.send(msg.encode(encoding))
			except BrokenPipeError:
				print(f"{self.address[0]}:{self.address[1]} || Client disconnected.")
				msg = msg.replace("\"", "'")
				return f"{self.address[0]}:{self.address[1]} || Failed to send \"{msg}\"."
			msg = msg.replace("\"", "'")
			return f"{self.address[0]}:{self.address[1]} || Sent \"{msg}\"."

		def recv(self, encoding="utf8"):
			data = self.client.recv(self.buffer).decode(encoding)
			return data

		def run(self):
			print(self.send(f"Connected to server \"{self.host}\"."))
			while True:
				msg = self.recv()
				if not msg:
					break
				print(f"{self.host}:{self.address[1]} || Recieved \"{msg}\" from \"{self.address[0]}\".")
				if msg[:8] == "https://":
					print("Testing link...")
					threaded_download = Thread(target=download.download, args=(msg,))
					threaded_download.start()
			print(f"{self.address[0]}:{self.address[1]} || Client disconnected.")

class Server:
	def __init__(self, address=cfg.local_server_address, port=cfg.server_port):
		self.host = address
		self.port = port
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def accept(self):
		client, address = self.s.accept()
		print(f"{address[0]}:{address[1]} || New client connection accepted.")
		return client, address

	def listen(self, max_connections=cfg.max_connections):
		print(f"{self.host}:{self.port} || Binding to IPv4...")
		try:
			self.s.bind((self.host, self.port))
		except OSError:
			self.s.close()
			self.s.bind((self.host, self.port))
		print(f"{self.host}:{self.port} || Listnening for connections...")
		self.s.listen(max_connections)

	def run(self):
		threaded_bot = Thread(target=start_bot)
		threaded_bot.start()

		print("DEBUG: started bot!")
		cfg.reset_attempts()
		self.listen()
		while True:
			client, address = self.accept()
			threaded_client = Thread(target=on_new_user, args=(client,address,self.host))
			threaded_client.start()
