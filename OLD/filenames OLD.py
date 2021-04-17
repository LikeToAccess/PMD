# -*- coding: utf-8 -*-
# filename          : filenames.py
# description       : Re-name files to their correct versions
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 12-01-2020
# version           : v1.0
# usage             : python main.py
# notes             : 
# license           : MIT
# py version        : 3.7.8 (must run on 3.6 or higher)
#==============================================================================
from shutil import move
import os

def copy(filename, destination):
	try:
		move(filename, f"{destination}/{filename}")
		print(f"MOVE: {filename} -> {destination}")
	except Exception as e:
		print(f"The file failed to move with the following exception:\n{filename}: {e}")

def rename(file, new_file):
	new_file = new_file.split(".")
	if "crdownload" in new_file:
		raise Exception("File is not done downloading!")
	new_file = new_file[0].strip() + "." + new_file[1]
	os.rename(file, new_file)
	print(f"RENAME: {file} -> {new_file}")

def check_name(file):
	if "-" in file or "_" in file or "1080" in file or "720" in file or "360" in file and file.split():
		return True
	else:
		return False

def main(path):
	os.chdir(f"X:/PLEX/TEMP/{path}")
	files = os.listdir()
	new_path = f"../../{path}"
	for file in files:
		try:
			split_file = file.split("-")
			# breaking-bad-season-1-episode-07-a-no-rough-stuff-type-deal_360.mp4
			# breaking bad - S01E07 - a no rough stuff type deal.mp4
			if "season" in file and "episode" in split_file:
				text = " ".join(split_file)
				season = text.split("season")
				episode = text.split("episode")
				show_title = "".join(season[0]).strip()
				season = "".join(season[1][1])
				season = season if len(season) > 1 else f"0{season}"
				episode_title = "".join(episode[1][3:]).strip()
				episode = "".join(episode[1][1:3])
				try:
					os.mkdir(f"X:/PLEX/TV SHOWS/{show_title}")
				except OSError:
					pass
				try:
					os.mkdir(f"X:/PLEX/TV SHOWS/{show_title}/Season {season}")
				except OSError:
					pass
				new_path = f"X:/PLEX/TV SHOWS/{show_title}/Season {season}"
				new_file = f"{show_title} - S{season}E{episode} - {episode_title}"\
				.replace("1080","") \
				.replace("720","")  \
				.replace("360","")  \
				.replace("_","")    \
				.strip()
			elif check_name(file):
				new_file = file     \
				.replace("1080","") \
				.replace("720","")  \
				.replace("360","")  \
				.replace("-"," ")   \
				.replace("_","")    \
				.strip()
			else:
				pass
			rename(file, new_file)
			file = new_file
			copy(file, new_path)
		except Exception as e:
			print(f"The code failed to execute with the following exception:\n{file}: {e}")

main(path="MOVIES")
main(path="TV SHOWS")
