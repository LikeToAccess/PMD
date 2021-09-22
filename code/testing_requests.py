import requests

# proxies = {
# 	"https": "http://45.86.68.164:8888"
# }

proxies = {
	# "http": "http://195.158.197.13:1043",
	"https": "https://195.158.197.13:1043"
}

# proxies = {
# 	"http":  "http://40.91.94.165:3128",
# 	"https": "https://159.203.84.241:3128"
# }


resp = requests.get('http://gomovies-online.cam/', proxies=proxies)
# resp = requests.get('http://example.org')
status_code = resp.status_code
print(f"STATUS: {status_code}")
