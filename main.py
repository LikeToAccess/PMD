# -*- coding: utf-8 -*-
# filename          : main.py
# description       : Easily download movies onto a server
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 04-14-2021
# version           : v1.0
# usage             : python main.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
from server import Server


server = Server(address="10.200.10.200")
# server = Server()


if __name__ == "__main__":
	pass
	# server.run()



import requests
response = requests.get(
		"https://stream-2-1-ip6.loadshare.org/slice/5/VideoID-JQemxbRJ/Ft6nSI/wJXX0K/VapEGu/JiuPxt/360?name=nobody-2021_360&token=ip=2600:1014:b06d:7731:61c5:42df:4f66:4b9~st=1618589323~exp=1618603723~acl=/*~hmac=a23a264ff8356ee7075f2f20d7c3f69b38a6d11443df9c807eba6b42886ce91a",
		params={
			"name": "nobody-2021_360",
			"token": "ip=209.237.96.178~st=1618590435~exp=1618590495~acl=/*~hmac=d1b9c1947ff8577fed9a36628635843665f75641bcdebe69d43bf6b2a6e4f021"

		},
		headers={
			":authority": stream-2-1-ip4.loadshare.org
			":method": GET
			":path": /slice/5/VideoID-JQemxbRJ/Nn6wSR/OFXx0y/sypjGH/BKufxy/360?name=nobody-2021_360&token=ip=209.237.96.178~st=1618590435~exp=1618590495~acl=/*~hmac=d1b9c1947ff8577fed9a36628635843665f75641bcdebe69d43bf6b2a6e4f021
			":scheme": https
			"accept": */*
			"accept-encoding": identity;q=1, *;q=0
			"accept-language": en-US,en;q=0.9,es;q=0.8
			"dnt": 1
			"range": bytes=0-
			"referer": https://gomovies-online.cam/
			"sec-ch-ua": "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"
			"sec-ch-ua-mobile": ?0
			"sec-fetch-dest": video
			"sec-fetch-mode": no-cors
			"sec-fetch-site": cross-site
			"user-agent": Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36
		}
	)
if response.status_code == 200:
	print('Success!')
elif response.status_code == 404:
	print('Not Found.')
else:
	print(response.status_code)
# request = requests.get(url, allow_redirects=True)
# with open("movie.mp4", "wb") as f:
# 	f.write(request.content)


#url = "https://stream-2-1-ip6.loadshare.org/slice/5/VideoID-JQemxbRJ/Ft6nSI/wJXX0K/VapEGu/JiuPxt/360?name=nobody-2021_360&token=ip=2600:1014:b06d:7731:61c5:42df:4f66:4b9~st=1618589323~exp=1618603723~acl=/*~hmac=a23a264ff8356ee7075f2f20d7c3f69b38a6d11443df9c807eba6b42886ce91a"

'''fetch("https://stream-2-1-ip4.loadshare.org/slice/5/VideoID-JQemxbRJ/Nn6wSR/OFXx0y/sypjGH/BKufxy/360?name=nobody-2021_360&token=ip=209.237.96.178~st=1618590435~exp=1618590495~acl=/*~hmac=d1b9c1947ff8577fed9a36628635843665f75641bcdebe69d43bf6b2a6e4f021", {
  "headers": {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,es;q=0.8",
    "range": "bytes=0-",
    "sec-ch-ua": "\"Google Chrome\";v=\"89\", \"Chromium\";v=\"89\", \";Not A Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-fetch-dest": "video",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site"
  },
  "referrer": "https://gomovies-online.cam/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": null,
  "method": "GET",
  "mode": "cors",
  "credentials": "omit"
});'''
