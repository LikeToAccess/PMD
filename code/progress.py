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
from time import time, strftime, gmtime
import download
import media
from media import log


def file_size(filename, count, start_time=None, target_size=None):
	target_size = int(target_size)
	size = download.size(filename)
	rounded_size = round(size/1024/1024, 2)
	# print(f"DEBUG: tg_s:{target_size}, s:{size}, r_s:{rounded_size}")
	if ((count+1) % 25 == 0 or count == 3) and start_time and target_size:
		filename = media.format_title(filename)
		speed = round(rounded_size/(time()-start_time) * 8, 2)
		# print(f"DEBUG: {(target_size-size)/(speed/8*1024*1024)}<-- ETA in s")
		eta = strftime("%Hh %Mm %Ss", gmtime((target_size-size)/(speed/8*1024*1024)))
		rounded_size, target_size = int(rounded_size), int(target_size/1024/1024)
		msg = f"Downloading {filename} at ~{speed} Mbps, ETA: {eta} ({rounded_size}/{target_size} MB)."
		# print(msg)
		log(msg, silent=False)

	return size
