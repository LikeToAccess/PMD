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
	resolution = quality[int(resolution)]
	with request as r:
		r.raise_for_status()
		with open(filename, "wb") as file:
			msg = f"Downloading {media.format_title(filename)} in {resolution}p..."
			print(msg)
			log(msg)
			cfg.reset_attempts()
			for count, chunk in enumerate(request.iter_content(chunk_size=chunk_size)):
				file.write(chunk)
				progress.file_size(filename, count, start_time=start_time)

	return filename
