# -*- coding: utf-8 -*-
# filename          : client.py
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
from time import sleep
import socket
import webbrowser
import os

# unused ports: 26490-26999
port = 26490
address = "192.168.50.209"

try: os.chdir("X:\\PLEX\\MOVIES")
except OSError as e: print(f"Unable to change directory, CWD: {os.getcwd()}")

# with open("X:/PLEX/config.ini", "r") as f:
# 	lines = f.read().split("\n")
# quality = lines[0]
quality = "1080"

def cmd(command):
    if command[:2] == "cd":
        os.chdir(command[2:])
    elif command == "refresh":
    	os.system("python X:/PLEX/TEMP/filenames.py")
    else:
        os.system(command)

def connect(address="192.168.50.204", port=26490):
    print("Connecting to \"{0}:{1}\"...".format(address,port))
    s.connect((address, port))
    print("Connected!")

def send(msg):
    clientsocket, address = s.accept()
    newThang = input("Enter stuf:")

def recv(buffer=1024):
    msg = s.recv(buffer)
    return msg.decode("utf8")

def download(url):
	with open("X:/PLEX/config.ini", "r") as f:
		lines = f.read().split("\n")
	quality = lines[0]
	#https://stream-2-1-ip4.loadshare.org/slice/6/VideoID-eWCuhoFL/o53J0V/ze9wqv/zgXbIp/aSuPDq/360?name=wonder-woman-2017_360&token=ip=75.72.179.246~st=1607149258~exp=1607163658~acl=/*~hmac=c105450296b8befab6c07ee4f89353668f60277a48545a7401bb97e9efbee17e
	#wonder-woman-2017_1080 -> wonder woman 2017
	url = url.replace("/360?name=",f"/{quality}?name=").replace("_360&token=ip=",f"_{quality}&token=ip=")
	filename = url.split("?name=")[1].split("&token=ip=")[0]
	new_filename = filename.strip(f"_{quality}").replace("-", " ")
	print(f"{filename} -> {new_filename}")
	os.system("python X:/PLEX/TEMP/filenames.py")
	webbrowser.open(url, autoraise=False)

while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connect(address=address, port=port)

		print(recv())

		running = True
		while running:
			url = recv()
			if url == "":
				socket.close()
			print("Received URL:\n> {0}".format(url))
			if url[:4] == "http":
				download(url)
			else:
				cmd(url)
	except Exception as e:
		print(e)
		sleep(10)
