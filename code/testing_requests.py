import requests


proxies = {
	"http":  "socks5://192.168.50.99:28284",
	"https": "socks5://192.168.50.99:28284",
	# "http://example.org": "socks5://192.168.50.99:28284"
}
headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0"}
url = "https://gomovies-online.cam/"


resp = requests.get(url, proxies=proxies, headers=headers)
status_code = (f"GOOD ({resp.status_code})" if resp.status_code == 200 else f"BAD ({resp.status_code})")
# print(resp.text)
print(f"STATUS for \"{url}\": {status_code}.")
