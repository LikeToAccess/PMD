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
import os
from threading import Thread
import requests
from requests.exceptions import *
from urllib3.exceptions import SSLError
from scraper import Scraper
from stream import Stream
import config as cfg
import media
from media import log


headers = {"user-agent": cfg.user_agent}
resolution_list = cfg.video_quality
media_files = media.Media("MOVIES")
home = os.getcwd()
requests.adapters.HTTPAdapter(max_retries=cfg.max_retries)


def url_format(url, target_res, old_res="360"):
	url = url.replace(f"/{old_res}?name=",f"/{target_res}?name=")
	url = url.replace(f"_{old_res}&token=ip=",f"_{target_res}&token=ip=")
	return url

def validate_url(url, target_res=None):
	if target_res:
		url = url_format(url, target_res)
	error_message = ""
	try:
		request = requests.get(
			url,
			headers=headers,
			proxies=(cfg.proxy if cfg.proxy else None),
			stream=True,
			timeout=(30,60)
		)
		status_code = request.status_code
	except ConnectionError:
		error_message = " (check the port on the proxy?)"
		status_code = 403
		request = None
	print(f"STATUS for {target_res}p: {status_code}{error_message}" if target_res else None)
	return status_code, request


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
		for target_res in resolution_list:  # TODO: The proccess of checking every resolution's status code takes too long (fix me)
			valid_resolution, request = validate_url(url, target_res)
			valid_resolutions.append(valid_resolution)
			if valid_resolutions[-1] == 200:
				url = url_format(url, target_res)
				break
			if valid_resolutions[-1] == 403:
				filmname = self.metadata["data-filmname"]
				log(f"ERROR: Link expired while scraping \"{filmname}\".")
				return False, None, None
		if 200 not in valid_resolutions:
			log(f"ERROR: Status code {valid_resolutions[-1]}.")
			return False, None, None
		return url, request, target_res

	def run(self, resolution_override=None):
		# Function should return True when the download is complete and False if it perminantly failed
		self.url, request, resolution = self.best_quality(self.url)
		if self.url is False:
			return False

		filmname = self.metadata["data-filmname"]
		year = self.metadata["data-year"]
		if "Season" in filmname and "Episode" in filmname:
			print("Media is detected as TV Show.")
			show_title =    filmname.split(" - ")[0]
			season =        filmname.split(" - Season ")[1].split(" Episode")[0].split(" [")[0]
			season =        season if len(season) >= 2 else "0" + season
			episode =       filmname.split(" Episode ")[1].split(": ")[0]
			try:
				episode_title = filmname.split(": ")[(1 if " [" not in filmname else 2)]
				# filename =      f"{show_title} - s{season}ep{episode} - {episode_title}"
				filename =      f"{show_title} - s{season}ep{episode}"
			except IndexError:
				filename =      f"{show_title} - s{season}ep{episode}"
			absolute_path = os.path.abspath(
				f"../TV SHOWS/{show_title}/Season {season}/{filename}.crdownload"
			)
		else:
			print("Media is detected as Movie/Film.")
			filename = (f"{filmname} ({year})" if filmname[-1] != ")" else filmname)
			absolute_path = os.path.abspath(f"../MOVIES/{filename}/{filename}.crdownload")
		stream = Stream(
			request,
			absolute_path,
			(
				resolution_override if resolution_override else resolution
			),
		)
		stream.stream()
		filename = filename.replace(".crdownload", ".mp4")
		file_size = round(int(request.headers.get("content-length", 0))/1024/1024,2)
		media.credit(self.author, filename=filename, resolution=resolution, file_size=file_size)
		log(f"Finished download of {filename} in {resolution}p ({file_size} MB).", silent=False)

		return True


if __name__ == "__main__":
	def run_download(url, metadata, author):
		download_function = Download(url, metadata, author)
		threaded_download = Thread(target=download_function.run)
		threaded_download.start()

	scraper = Scraper(minimize=False)
	search = input("Enter a Title to search for:\n> ")

	while search:
		download_queue = scraper.download_first_from_search(search)
		if download_queue:
			for data in download_queue:
				if None in data:
					log("No results!", silent=False)

				run_download(data[0], data[1][list(data[1])[0]], data[2])
				search = input("Enter a Title to search for:\n> ")
		else:
			log("No results!", silent=False)
