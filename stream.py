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
import time
import os
import config as cfg
import progress
import media
from media import log


headers = {"user-agent": cfg.user_agent}
quality = cfg.video_quality


class Stream:
	def __init__(self, request, filename, resolution, chunk_size=cfg.stream_chunk_size):
		filename = filename.replace("\\", "/")
		self.request = request
		self.filename = (
			"/".join(filename.split("/")[:1]) + "/".join(filename.split("/")[1:]).replace(":", "")
		) if "exe" in cfg.executable else filename
		self.resolution = resolution
		self.chunk_size = chunk_size
		self.target_size = int(request.headers.get("content-length", 0))

	def write(self):
		self.verify_path()
		with open(self.filename, "wb") as file:
			title = self.filename.split(".")[0]
			size_MB = round(self.target_size/1024/1024,2)
			start_time = time.time()
			msg = f"Downloading {title} in {self.resolution}p ({size_MB} MB)..."
			log(msg, silent=False)
			try:
				for count, chunk in enumerate(self.request.iter_content(chunk_size=self.chunk_size)):
					file.write(chunk)
					progress.file_size(
						self.filename,
						count,
						start_time,
						target_size=self.target_size
					)
			# except ConnectionResetError as e:
			except Exception as e:
				log(f"ERROR with {title}: Connection Reset!\nRetrying download...")
				log(str(e))
				self.write()

	def verify_path(self):
		path = "/".join(self.filename.split("/")[:-1])
		path_exists = os.path.isdir(path)
		if not path_exists:
			# print(f"DEBUG: {self.filename}")
			# print(f"DEBUG: {path}")
			os.makedirs(path)
		return path_exists

	def stream(self):
		with self.request as r:
			# print("DEBUG: raise_for_status")
			r.raise_for_status()
			# print("DEBUG: self.write")
			self.write()
			# print("DEBUG: media.rename")
			print(media.rename(self.filename, self.filename.replace(".crdownload",".mp4")))
			# size_MB = round(self.target_size/1024/1024,2)
			# log(f"Finished download of {self.filename} in {self.resolution}p ({size_MB} MB).")
			# media.credit(author, filename=filename, resolution=resolution, file_size=file_size)


if __name__ == "__main__":
	print(Stream(None, "MOVIES/Black Widow (2021)/Black Widow (2021).crdownload", 1080).verify_path())
