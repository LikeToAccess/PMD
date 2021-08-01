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
import time
import os
from scraper import Scraper
import requests as req
from requests.exceptions import *
from urllib3.exceptions import SSLError
import config as cfg
import stream
import media
from media import log


headers = {"user-agent": cfg.user_agent}
quality = cfg.video_quality
media_files = media.Media("MOVIES")
home = os.getcwd()
req.adapters.HTTPAdapter(max_retries=2)
start_time = 0


def make_directory():
	if media_files.path != "MOVIES":
		root_path = media_files.path.split("/")[0]
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}"): os.mkdir(root_path + \
			f"/{media_files.show_title}")
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}"): os.mkdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}")

def size(filename):
	file_size = os.stat(filename).st_size
	return file_size

def download(url, metadata, author):
	# Function should return True when the download is complete and False if it perminantly failed
	if not url:
		log("ERROR: No URL! Maybe there were no search results?", silent=False)
		return False
	if not isinstance(url, str):
		url = url.get_attribute("src")

	print(f"URL:      {url}")
	print(f"METADATA: {len(metadata)}")
	print(f"AUTHOR:   {author}")
	# print(url == str(url))

	return True


if __name__ == "__main__":
	scraper = Scraper()
	data = scraper.download_first_from_search(input("Enter a Title to search for:\n> "))
	download(data[0], data[1], "0")
