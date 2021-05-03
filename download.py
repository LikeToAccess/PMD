from time import time
import os
import sys
import requests as req
import config as cfg
import stream
import media


headers = {"user-agent": cfg.user_agent}
quality = cfg.video_quality
media_files = media.Media("MOVIES")
home = os.getcwd()
req.adapters.HTTPAdapter(max_retries=2)


def url_format(url, target_res):
	for current_res in quality:
		url = url.replace(f"/{current_res}?name=",f"/{quality[int(target_res)]}?name=")
		url = url.replace(f"_{current_res}&token=ip=",f"_{quality[int(target_res)]}&token=ip=")
	return url

def test_link(url, start_time=0, resolution=0, error=False):
	if ((time() - start_time) < 10) or error:
		if int(resolution) >= len(quality)-1:
			error = "FAILED (cannot lower quality)\nFailed download, link is invalid."
			print(error)
			os.system(f"python3 bot.py \"{error}\"")
			cfg.reset_attempts()
			return False
		cfg.increment_attempts()
		print("FAILED (lowering quality)")
		download(url)
		return False
	print("FAILED (retrying)")
	os.system("python3 bot.py FAILED (retrying)")
	download(url)
	return False

def size(filename):
	file_size = os.stat(filename).st_size
	return file_size

def download(url):
	# os.system(f"python3 bot.py \"{data}"\")
	resolution = cfg.read_attempts()
	try: url = url_format(url, resolution)
	except IndexError as error:
		return test_link(url, resolution=resolution, error=error)
	try: filename = media_files.rename(url.split("?name=")[1].split("&token=ip=")[0]+".mp4")
	except IndexError: filename = False
	try: request = req.get(url, headers=headers, stream=True, timeout=(cfg.timeout/2,cfg.timeout))
	except (req.exceptions.ConnectionError, req.exceptions.InvalidURL, req.exceptions.ReadTimeout):
		print("DEBUG: error")
		filename = False
	if not filename:
		error = f"FAILED (download timed out {cfg.timeout}s)\nFailed download, link is invalid."
		print(error)
		os.system(f"python3 bot.py \"{error}\"")
		return False
	msg = f"Atempting download in {quality[int(resolution)]}p..."
	print(msg, end=" ", flush=True)
	os.system(f"python3 bot.py {msg}")
	start_time = time()
	# print(f"DEBUG: {request.headers}")
	# print(f"DEBUG: {request}, {filename}, {media_files.path}, {url}")
	absolute_path = f"{media_files.path}/{filename}"
	if media_files.path != "MOVIES":
		root_path = media_files.path.split("/")[0]
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}"): os.mkdir(root_path + \
			f"/{media_files.show_title}")
		if not os.path.isdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}"): os.mkdir(root_path + \
			f"/{media_files.show_title}/Season {media_files.season}")

	try: stream.download_file(request, absolute_path)
	except req.exceptions.ConnectionError:
		download(url)
		os.system("python3 bot.py Error Unknown")
		return False
	except req.exceptions.HTTPError as error:
		return test_link(url, error=error)
	file_size = size(absolute_path)
	if file_size == 0:
		return test_link(url, start_time, resolution)
	with open(absolute_path, "r") as file:
		try:
			for count, line in enumerate(file):
				if count > 20:
					break
				if "403 Forbidden" in line:
					return test_link(url, start_time, resolution)
		except UnicodeDecodeError:
			pass
	cfg.reset_attempts()
	final_msg = f"Finished download of {absolute_path} in {quality[int(resolution)]}p ({size(absolute_path)/1024/1024} MB.)"
	print(final_msg)
	os.system(f"python3 bot.py \"{final_msg}\"")
	return final_msg


if __name__ == "__main__":
	if sys.argv[1]:
		download(sys.argv[1])
	else:
		print("No URL specified.")
