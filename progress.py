import sys
from time import sleep


bar_width = 25

def test():
	while True:
		sys.stdout.write("Downloading Movie...\n[{0}] 40MB Chunk".format(" " * bar_width,"test"))
		sys.stdout.flush()
		sys.stdout.write("\b" * (bar_width+1+11))
		for i in range(bar_width):
			sleep(0.2)
			sys.stdout.write("-")
			sys.stdout.flush()

	sys.stdout.write("] 40.0MB Chunk\n")


if __name__ == "__main__":
	test()
