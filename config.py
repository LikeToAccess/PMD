# [IMPORTS]
import socket
import os


#
# [NETWORKING]
#
local_server_address = socket.gethostbyname(socket.gethostname())
remote_server_address = "127.0.0.1"
server_port = 26490
network_buffer = 1024
max_connections = 5
max_retries = 2
proxy = False
# proxy = {
# 	"http":  "socks5://192.168.50.98:9667",
# 	"https": "socks5://192.168.50.98:9667"
# }


#
# [DOWNLOAD OPTIONS]
#
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
# video_quality = [2160, 1440, 1080, 720, 480, 360]
video_quality = [2160, 1440, 1080, 720, 480, 360]
stream_chunk_size = 8*1024*1024
timeout = 60
executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"



# [FUNCTIONS]
def reset_attempts():
	buffer = []
	with open("config.py", "r") as file:
		lines = file.read().split("\n")
	for line in lines:
		if line[:20] == "download_attempts = ":
			line = "download_attempts = 0"
		buffer.append(line)
	with open("config.py", "w") as file:
		file.write("\n".join(buffer))

def read_attempts():
	with open("config.py", "r") as file:
		lines = file.read().split("\n")
	for line in lines:
		if line[:20] == "download_attempts = ":
			return line[20:]
	return False

def increment_attempts():
	buffer = []
	with open("config.py", "r") as file:
		lines = file.read().split("\n")
	for line in lines:
		if line[:20] == "download_attempts = ":
			line = f"download_attempts = {int(line[20:])+1}"
		buffer.append(line)
	with open("config.py", "w") as file:
		file.write("\n".join(buffer))

def write_attempts(count):
	buffer = []
	with open("config.py", "r") as file:
		lines = file.read().split("\n")
	for line in lines:
		if line[:20] == "download_attempts = ":
			line = f"download_attempts = {count}"
		buffer.append(line)
	with open("config.py", "w") as file:
		file.write("\n".join(buffer))
