# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Reorganize and rename music files for Plex
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 02-28-2022
# version           : v1.0
# usage             : python main.py
# notes             : https://support.plex.tv/articles/200265296-adding-music-media-from-folders/
# license           : MIT
# py version        : 3.10.2 (must run on 3.6 or higher)
#==============================================================================
import os
import shutil
from music_settings import *


class Song:
	def __init__(self, audio_file, source_path=SOURCE_PATH):
		split_by_character = " - "
		self.audio_file_path = os.path.abspath(os.path.join(source_path,audio_file))
		self.audio_file = audio_file
		self.artist_name = audio_file.split(split_by_character)[0]
		self.album_name = None
		self.track_name = split_by_character.join(audio_file.split(split_by_character)[1:])
		self.source_path = self.audio_file_path

	def move(self, destination_path=DESTINATION_PATH):
		destination_path = \
			f"{destination_path}/{self.artist_name}/{self.album_name if self.album_name else ''}"
		destination_path = os.path.join(destination_path, self.track_name.rsplit('.',1)[0])
		if not os.path.exists(destination_path):
			os.makedirs(destination_path)

		destination_path = os.path.join(destination_path, self.track_name)
		shutil.move(self.source_path, destination_path)

	def copy(self, destination_path=DESTINATION_PATH):
		destination_path = \
			f"{destination_path}/{self.artist_name}/{self.album_name if self.album_name else ''}"
		destination_path = os.path.join(destination_path, self.track_name.rsplit('.',1)[0])
		if not os.path.exists(destination_path):
			os.makedirs(destination_path)

		destination_path = os.path.join(destination_path, self.track_name)
		shutil.copy(self.source_path, destination_path)


def main():
	audio_files = os.listdir(os.path.abspath(SOURCE_PATH))
	for audio_file in audio_files:
		if audio_file.split(".")[-1] not in VALID_AUDIO_FILE_FORMATS:
			continue
		print(f"{audio_file} was moved succesfully.")
		Song(audio_file).move()


if __name__ == "__main__":
	main()
