import sys
from time import sleep
import config as cfg
import download

bar_width = 45

def progress_bar(progress="new"):
	if progress == 0:
		sys.stdout.write("[{0}]".format(" "*bar_width))
		sys.stdout.flush()
		sys.stdout.write("\b" * (bar_width+1))
	elif progress == "new":
		sys.stdout.write("\b" * (bar_width+58))
		sys.stdout.flush()
	elif progress == "finish":
		print("] 40.0MB ")
	elif progress > 0:
		sys.stdout.write("=")
		amount = str(round(progress/bar_width,1))
		sys.stdout.write(" "*(bar_width-progress) + f"] {float(amount)*40}MB ")
		sys.stdout.write("\b" * (bar_width-progress+len(f"] {float(amount)*40}MB ")))
		sys.stdout.flush()

def file_size(filename, count):
	size = download.size(filename)
	if count == 1:
		sys.stdout.write(f"{size/1024/1024} MB")
		sys.stdout.flush()
	elif count >= 2:
		sys.stdout.write("\b"*int(size/1024/1024+3))
		sys.stdout.write(f"{size/1024/1024} MB")
		sys.stdout.flush()

if __name__ == "__main__":
	print("Downloading Movie...")
	for i in range(45):
		sleep(0.2)
		progress_bar(i)
	progress_bar("finish")
