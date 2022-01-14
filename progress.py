# -*- coding: utf-8 -*-
# filename          : progress.py
# description       : Feedback on the speed and progress of a download
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-04-2021
# version           : v1.1
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import time
import media
from media import log


def file_size(filename, count, start_time=None, target_size=None):
	size = media.size(filename)
	size_MB = round(size/1024/1024, 2)
	if ((count+1) % 25 == 0 or count == 3) and start_time and target_size:
		filename = media.format_title(filename)
		remaining_size = target_size-size
		speed = size/(time.time()-start_time)
		speed_MB = round(speed*8/(1024*1024), 2)
		ETA = time.strftime("%Hh %Mm %Ss", time.gmtime(remaining_size/speed))
		size_MB, target_size = int(size_MB), int(target_size/1024/1024)
		msg = f"Downloading {filename} at ~{speed_MB} Mbps, ETA: {ETA} ({size_MB}/{target_size} MB)."
		log(msg, silent=False)
	return size


if __name__ == "__main__":
	start_time_debug = time.time()
	time.sleep(1)
	file_size("chromedriver", 3, start_time_debug-time.time(), 100000000)
