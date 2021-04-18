import requests as req


headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
quality = "1080"


def download(url):
	url = url \
		.replace("/360?name=",f"/{quality}?name=") \
		.replace("_360&token=ip=",f"_{quality}&token=ip=")
	filename = url \
		.split("?name=")[1] \
		.split("&token=ip=")[0] \
		+ ".mp4"
	request = req.get(url, headers=headers, stream=True)
	stream_data(request, filename)

def stream_data(request, filename, chunk_size=4096):
	with open(filename, "wb") as file:
		for chunk in request.iter_content(chunk_size=chunk_size):
			file.write(chunk)
		return filename
	return False
