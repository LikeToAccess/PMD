# -*- coding: utf-8 -*-
# filename          : progress.py
# description       : Feedback on the speed and progress of a download
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-04-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
from time import time
import download
import media
from media import log


def file_size(filename, count, start_time=None):
	size = download.size(filename)
	size = round(size/1024/1024, 2)
	if (count+1 % 25 == 0 or count == 4) and start_time:
		filename = media.format_title(filename)
		speed = round(size/(time()-start_time)*8, 2)
		msg = f"Downloading {filename} at ~{speed} Mbps ({size} MB total)."
		print(msg)
		log(msg)
	return size
