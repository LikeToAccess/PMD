import sys
import config as cfg
import download


bar_width = 40
headers = {"user-agent": cfg.user_agent}


def download_file(request, filename="MOVIE.mp4", chunk_size=cfg.stream_chunk_size):
	sys.stdout.write("[%s]" % (" " * bar_width))
	sys.stdout.flush()
	sys.stdout.write("\b" * (bar_width+1))
	with request as r:
		r.raise_for_status()
		with open(filename, 'wb') as file:
			for count, chunk in enumerate(request.iter_content(chunk_size=chunk_size)):
				file.write(chunk)
				if count % 6 == 0:
					print(f"{round(download.size(filename)/(1024*1024),2)}MB downloaded.")
				sys.stdout.write("-")
				sys.stdout.flush()
	sys.stdout.write("]\n")
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
