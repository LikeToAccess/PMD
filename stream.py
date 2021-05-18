# -*- coding: utf-8 -*-
# filename          : stream.py
# description       : Does the actual streaming and IO operations
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-04-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import config as cfg
import progress
from media import log
import media


headers = {"user-agent": cfg.user_agent}
quality = cfg.video_quality


def download_file(request, filename, resolution, chunk_size=cfg.stream_chunk_size, start_time=None):
	target_size = request.headers.get("content-length", 0)
	# log(f"DEBUG: Target Size is {target_size}.")
	resolution = quality[int(resolution)]
	with request as r:
		r.raise_for_status()
		with open(filename, "wb") as file:
			title = media.format_title(filename)
			msg = f"Downloading {title} in {resolution}p ({round(int(target_size)/1024/1024,2)} MB)..."
			print(msg)
			log(msg)
			cfg.reset_attempts()
			for count, chunk in enumerate(request.iter_content(chunk_size=chunk_size)):
				file.write(chunk)
				progress.file_size(filename, count, start_time=start_time, target_size=target_size)

	return filename
