import os
import config as cfg
import progress
from media import log


headers = {"user-agent": cfg.user_agent}


def download_file(request, filename="MOVIE.mp4", chunk_size=cfg.stream_chunk_size, start_time=None):
	with request as r:
		r.raise_for_status()
		with open(filename, "wb") as file:
			msg = "IN-PROGRESS"
			print(msg)
			# os.system(f"python3 bot.py {msg}")
			log(msg)
			for count, chunk in enumerate(request.iter_content(chunk_size=chunk_size)):
				file.write(chunk)
				progress.file_size(filename, count, start_time=start_time)
				# if count <= 45:
				# 	progress.progress_bar(count)
				# else:
				# 	progress.progress_bar(count-45*(count/45))
				# if count % 5 == 0:
				# 	print(f"{round(download.size(filename)/(1024*1024),2)}MB downloaded.")
	return filename

# def stream_data(request, filename, chunk_size=cfg.stream_chunk_size):
# 	count = 0
# 	with open(filename, "wb") as file:
# 		for chunk in request.iter_content(chunk_size=chunk_size):
# 			if chunk:
# 				file.write(chunk)
# 				count += 1
# 				if count == 2:
# 					print("IN PROGRESS (currently downloading)")
# 				if count % 10 == 0:
# 					print(f"{round(size(filename)/(1024*1024),2)}MB downloaded.")
# 		return filename
# 	print("DEBUG: Something went wrong in stream_data")
# 	return False
