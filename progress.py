# import sys
from time import time
import download
import media
from media import log

# bar_width = 45

# def progress_bar(progress="new"):
# 	if progress == 0:
# 		sys.stdout.write("[{0}]".format(" "*bar_width))
# 		sys.stdout.flush()
# 		sys.stdout.write("\b" * (bar_width+1))
# 	elif progress == "new":
# 		sys.stdout.write("\b" * (bar_width+58))
# 		sys.stdout.flush()
# 	elif progress == "finish":
# 		print("] 40.0MB ")
# 	elif progress > 0:
# 		sys.stdout.write("=")
# 		amount = str(round(progress/bar_width,1))
# 		sys.stdout.write(" "*(bar_width-progress) + f"] {float(amount)*40}MB ")
# 		sys.stdout.write("\b" * (bar_width-progress+len(f"] {float(amount)*40}MB ")))
# 		sys.stdout.flush()

def file_size(filename, count, start_time=None):
	size = download.size(filename)
	size = round(size/1024/1024, 2)
	if (count+1 % 100 == 0 or count == 4) and start_time:
		filename = media.format_title(filename)
		speed = round(size/(time()-start_time)*8, 2)
		msg = f"Downloading {filename} at ~{speed} Mbps ({size} MB total)."
		print(msg)
		log(msg)
	return size


# if __name__ == "__main__":
# 	print("Downloading Movie...")
# 	for i in range(45):
# 		sleep(0.2)
# 		progress_bar(i)
# 	progress_bar("finish"
