# -*- coding: utf-8 -*-
# filename          : media.py
# description       : Holds important functions for the project
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-04-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
from shutil import move
import os
import config as cfg


def log(msg):
	append_file("log.txt", msg)

def credit(author, filename, resolution, file_size):
	msg = f"{filename}|{resolution}|{file_size}"
	append_file(f"{author}.txt", msg)

def format_title(filename):
	if "/" in filename: filename = filename.split("/")[::-1][0]
	filename = " ".join([word.capitalize() for word in filename.split(".")[0].split()])
	return filename

def remove_file(filename):
	os.remove(filename)

def rename(filename_old, filename_new):
	filename = filename_new.split(".")
	filename_new = f"{filename[0].strip()}.{filename[1]}"
	try: os.rename(filename_old, filename_new)
	except FileExistsError:
		remove_file(filename_old)
		msg = f"Removed old version of show to be replaced with new version, {filename_new}"
		print(msg)
		log(msg)
		rename(filename_old, filename_new)
	return f"RENAME: {filename_old} -> {filename_new}"

def needs_formating(filename):
	for quality in cfg.video_quality:
		if (
			"-" in filename
			or "_" in filename
			and str(quality) in filename
		): return True
	return False

def read_file(filename, directory=None, filter=False):
	if directory:
		os.chdir(f"{os.getcwd()}/{directory}")
	with open(filename, "r") as file:
		lines = file.read().split("\n")
	if filter:
		lines = filter_list(lines)
	return lines

def write_file(filename, msg):
	with open(filename, "w") as file:
		file.write(msg)

def append_file(filename, msg):
	with open(filename, "a") as file:
		file.write(f"{msg}\n")

def filter_list(lines, filename=False):
	if filename:
		lines = read_file(filename)
	data = []
	for line in lines:
		if line[:1] != "#" and line != "":
			data.append(line)
	return data


class Media:
	def __init__(self, path):
		self.path = path
		self.season = False
		self.episode = False
		self.show_title = False
		self.episode_title = False

	def move(self, filename=None, show_title=None):
		os.chdir(f"X:/PLEX/TEMP/{self.path}")
		target_dir = f"../../{self.path}"
		if show_title:
			show_title, season = show_title
			try: os.mkdir(f"X:/PLEX/{self.path}/{show_title}")
			except OSError: pass
			try: os.mkdir(f"X:/PLEX/TV SHOWS/{show_title}/Season {season}")
			except OSError: pass
		if filename:
			files = [filename]
		else:
			files = os.listdir()
		for file in files:
			move(file, f"{target_dir}/{file}")

	def rename(self, filename):
		try:
			name = filename.replace("-", " ")
			names = filename.split("-")
			if "season" in names and "episode" in names and "_" in filename:
				self.season = name.split("season")[1].strip().split()[0]
				self.season = self.season if len(self.season) >= 2 else "0" + self.season
				self.episode = name.split("episode")[1].strip().split()[0]
				self.show_title = name.split("season")[0].strip()
				self.episode_title = name.split("episode")[1].replace(self.episode, "").strip().split("_")[0]
				self.path = f"TV SHOWS/{self.show_title}/Season {self.season}"
				filename = f"{self.show_title} - S{self.season}E{self.episode} - {self.episode_title}"
			elif needs_formating(filename):
				self.path = "MOVIES"
				for quality in cfg.video_quality:
					filename = filename            \
						.replace(str(quality), "") \
						.replace("-", " ")         \
						.replace("_", "")          \
						.split(".")[0]             \
						.strip()
			return filename + ".crdownload"
		except IndexError:
			pass
		return False
