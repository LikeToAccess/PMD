# -*- coding: utf-8 -*-
# filename          : main.py
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
from server import Server


# server = Server(address="10.200.10.200")
server = Server()


if __name__ == "__main__":
	server.run()
