# -*- coding: utf-8 -*-
# filename          : download.py
# description       : Handles downloading of movies
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


def url_format(url, target_res):
	for current_res in quality:
		url = url.replace(f"/{current_res}?name=",f"/{quality[int(target_res)]}?name=")
		url = url.replace(f"_{current_res}&token=ip=",f"_{quality[int(target_res)]}&token=ip=")
	return url

def test_link(url, author, start_time=0, resolution=0, filename=False, error=False):
	if filename: filename = media.format_title(filename)
	if ((time()-start_time) < 10) or error:
		if int(resolution) >= len(quality)-1:
			error = f"Failed download of {filename if filename else url}, link is invalid."
			print(error)
			log(error)
			cfg.reset_attempts()
			return False
		cfg.increment_attempts()
		# print("FAILED (lowering quality)")
		download(url, author=author)
		return False
	error = f"Failed download of {filename if filename else url}.\nRestarting download..."
	print(error)
	log(error)
	download(url, author=author)
	return False

def make_directory():
	if media_files.path != "MOVIES":
		root_path = media_files.path.split("/")[0]
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}"): os.mkdir(root_path + \
			f"/{media_files.show_title}")
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}"): os.mkdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}")

def check(url, base_url, author):
	resolution = cfg.read_attempts()
	try: url = url_format(url, resolution)
	except IndexError as error:
		return test_link(base_url if base_url else url, author=author, resolution=resolution, error=error)
	try: filename = media_files.rename(url.split("?name=")[1].split("&token=ip=")[0]+".crdownload")
	except IndexError:
		filename = False
		error = "This link does not go to a supported site!"
	try: request = req.get(url, headers=headers, stream=True, timeout=(cfg.timeout/2,cfg.timeout))
	except (req.exceptions.ConnectionError, req.exceptions.InvalidURL, req.exceptions.ReadTimeout):
		print("DEBUG: error")
		error = f"Connection error with {media.format_title(filename)}."
		filename = False
	if not filename:
		print(error)
		log(error)
		return False
	return filename, request, resolution

def size(filename):
	file_size = os.stat(filename).st_size
	return file_size

def download(url, author):
	global start_time

	data = check(url, base_url, author=author) if url else url
	print(data)
	if not data:
		error = "Scraping failed. Link is invalid or captcha was not solved."
		print(error)
		log(error)
		return False
	filename, request, resolution = data
	# msg = f"Atempting download in {quality[int(resolution)]}p..."
	# print(msg, end=" ", flush=True)
	# log(msg)
	target_size = request.headers.get("content-length", 0)
	rounded_target_size = round(int(target_size)/1024/1024,2)
	absolute_path = f"{media_files.path}/{filename}"
	make_directory()

	start_time = time()
	try: stream.download_file(request, absolute_path, resolution, start_time=start_time)
	except (ConnectionError, ConnectionResetError, ChunkedEncodingError, SSLError):
		log(f"Connection error while downloading {media.format_title(filename)}.\nRestarting download...")
		download(base_url if base_url else url, author=author)
		return False
	except req.exceptions.HTTPError as error: return test_link(base_url if base_url else url, author=author, error=error)
	file_size = round(size(absolute_path)/1024/1024, 2)
	if file_size == 0: return test_link(base_url if base_url else url, start_time, resolution)
	with open(absolute_path, "r") as file:
		try:
			for count, line in enumerate(file):
				if count > 20: break
				if "403 Forbidden" in line: return test_link(base_url if base_url else url, start_time, resolution)
		except UnicodeDecodeError: pass
	cfg.reset_attempts()
	filename = media.format_title(filename)
	resolution = quality[int(resolution)]
	if file_size != rounded_target_size:
		msg = f"{file_size}/{rounded_target_size} MB"
		msg = f"Error while downloading {filename}, incomplete file ({msg}).\nRestarting download..."
		print(msg)
		log(msg)
		download(base_url if base_url else url, author=author)
		return False
	else:
		final_msg = f"Finished download of {filename} in {resolution}p ({file_size} MB)."
		media.credit(author, filename=filename, resolution=resolution, file_size=file_size)
	complete = media.rename(absolute_path, absolute_path.replace(".crdownload",".mp4"))
	absolute_path = absolute_path.replace(".crdownload", ".mp4")
	if not complete:
		final_msg = f"Error while finishing {filename}, that file already exists.\nCould not complete."
	print(final_msg)
	log(final_msg)

	return final_msg
