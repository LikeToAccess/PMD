# -*- coding: utf-8 -*-
# filename          : download.py
# description       : Handles downloading of movies
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 08-01-2021
# version           : v2.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
# import time
import os
from scraper import Scraper
import requests
from requests.exceptions import *
from urllib3.exceptions import SSLError
from stream import Stream
import config as cfg
import media
from media import log


headers = {"user-agent": cfg.user_agent}
quality = cfg.video_quality
media_files = media.Media("MOVIES")
home = os.getcwd()
requests.adapters.HTTPAdapter(max_retries=2)


def url_format(url, target_res):
	for current_res in quality:
		url = url.replace(f"/{current_res}?name=",f"/{target_res}?name=")
		url = url.replace(f"_{current_res}&token=ip=",f"_{target_res}&token=ip=")
	return url

def validate_url(url, target_res):
	url = url_format(url, target_res)
	# print(f"URL:      {url}")
	# print(f"METADATA: {len(metadata)}")
	# print(f"AUTHOR:   {author}")
	# print(url == str(url))
	request = requests.get(url, headers=headers, stream=True, timeout=(30,60))
	status_code = request.status_code
	print(f"STATUS for {target_res}p: {status_code}")
	if status_code == 200:
		return True, request
	return status_code, request

# def make_directory():
# 	if media_files.path != "MOVIES":
# 		root_path = media_files.path.split("/")[0]
# 		if not os.path.isdir(root_path + f"/{media_files.show_title}"):
# 			os.mkdir(root_path + f"/{media_files.show_title}")
# 		if not os.path.isdir(root_path + f"/{media_files.show_title}/Season {media_files.season}"):
# 			os.mkdir(root_path + f"/{media_files.show_title}/Season {media_files.season}")


class Download:
	def __init__(self, url, metadata, author):
		self.url = url
		self.metadata = metadata
		self.author = author

	def best_quality(self, url):
		if not url:
			log("ERROR: No URL! Maybe there were no search results?", silent=False)
			return False, None, None
		if not isinstance(url, str):
			url = url.get_attribute("src")

		valid_resolutions = []
		for target_res in quality:
			valid_resolution, request = validate_url(url, target_res)
			valid_resolutions.append(valid_resolution)
			if valid_resolutions[-1] is True:
				url = url_format(url, target_res)
				break
			if valid_resolutions[-1] == "403":
				filmname = self.metadata["data-filmname"]
				log(f"ERROR: Link expired while scraping \"{filmname}\".")
				return False, None, None
		if True not in valid_resolutions:
			log(f"ERROR: Status code {valid_resolutions[-1]}.")
			return False, None, None
		return url, request, target_res

	def run(self, resolution_override=None):
		# Function should return True when the download is complete and False if it perminantly failed
		self.url, request, resolution = self.best_quality(self.url)
		if self.url is False:
			return False

		# print(f"DEBUG: {self.url}")
		# print(request.status_code)
		print(f"DEBUG: {self.metadata}")
		filmname = self.metadata["data-filmname"]
		year = self.metadata["data-year"]
		# print(f"DEBUG: {filmname}")
		if "Season" in filmname and "Episode" in filmname:
			print("Media is detected as TV Show.")
			show_title = filmname.split(" - ")[0]
			season = filmname.split(" - Season ")[1].split(" Episode")[0]
			season = season if len(season) >= 2 else "0" + season
			episode = filmname.split(" Episode ")[1].split(": ")[0]
			episode_title = filmname.split(": ")[1]
			filename = f"{show_title} - s{season}ep{episode} - {episode_title}"
			absolute_path = f"TV SHOWS/{show_title}/Season {season}/{filename}.crdownload"
		else:
			print("Media is detected as Movie/Film.")
			filename = f"{filmname} ({year})"
			absolute_path = f"MOVIES/{filename}/{filename}.crdownload"
		# print(absolute_path)
		# target_size = request.headers.get("content-length", 0)
		stream = Stream(
			request,
			absolute_path,
			(
				resolution_override if resolution_override else resolution
			),
		)
		# print(f"DEBUG: Starting the download for, {absolute_path}...")
		stream.stream()
		filename = filename.replace(".crdownload", ".mp4")
		file_size = round(int(request.headers.get("content-length", 0))/1024/1024,2)
		media.credit(self.author, filename=filename, resolution=resolution, file_size=file_size)
		log(f"Finished download of {filename} in {resolution}p ({file_size} MB).")

		return True


if __name__ == "__main__":
	scraper = Scraper(minimize=True)
	data = scraper.download_first_from_search(input("Enter a Title to search for:\n> "))
	if None in data:
		print("No results!")
		scraper.close()
		quit()
	# metadata[list(metadata)[0]]
	download = Download(data[0], data[1][list(data[1])[0]], "0")
	download.run()
