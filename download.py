import requests as req


url = "https://stream-2-1-ip4.loadshare.org/slice/5/VideoID-PF1eG5pI/tbbNoF/PRaFfu/JWYwzQ/wqXkei/360?name=invincible-season-1-episode-06-you-look-kinda-dead_360&token=ip=75.72.179.246~st=1618644960~exp=1618645020~acl=/*~hmac=35c7dda94e659a0ea24de8e4f4426f26e17589b9f4123564075da655e795ee90"
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"}
local_filename = "movie.mp4"


def main():
	r = req.get(url, headers=headers, stream=True)
	with open(local_filename, "wb") as f:
		for chunk in r.iter_content(chunk_size=1024):
			f.write(chunk)


if __name__ == "__main__":
	main()
