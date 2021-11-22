# -*- coding: utf-8 -*-
# filename          : scraper.py
# description       : Grabs movie links
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 07-15-2021
# version           : v2.0
# usage             : python scraper.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import time
import os
import sys
from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import crop
import media
import config as cfg
from errors import NoResults
from media import log


class Scraper:
	def __init__(self, minimize=True):
		options = Options()

		path = "Chrome Extensions"
		files = os.listdir(path)
		for file in files:
			if file.endswith("crx"):
				options.add_extension(os.path.abspath(path + "/" + file))

		# options.add_argument("headless")
		user_data_dir = os.path.abspath("selenium_data")
		options.add_argument(f"user-data-dir={user_data_dir}")
		options.add_argument("--disable-gpu")
		options.add_argument("log-level=3")
		self.driver = webdriver.Chrome(executable_path=os.path.abspath(cfg.executable), options=options)
		self.first_launch = True
		self.author = "0"
		self.headers = {"user-agent": cfg.user_agent}
		if minimize: self.driver.minimize_window()

	def search(self, url, media_type=0):
		if media_type == 0:  # Movie (HD)
			element_class = "item_hd"
			description_class = "_smQamBQsETb"
		elif media_type == 1:  # Movie (CAM)
			element_class = "item_cam"
			description_class = "_smQamBQsETb"
		elif media_type >= 2:  # TV Show
			element_class = "item_series"
			description_class = "_skQummZWZxE"
		self.open_link(url)
		results, descriptions = self.get_results_from_search(
			element_class=element_class,
			decription_class=description_class
		)

		if not results:
			if media_type >= 2:  # TV Show
				raise NoResults
			media_type += 1
			return self.search(url, media_type=media_type)

		if media_type == 1: log("**INFO:** Film is in CAM quality.", silent=False)
		if not descriptions:  # this is the same as "if results and not descriptions:"
			description_class = "_smQamBQsETb"
			results, descriptions = self.get_results_from_search(
				element_class=element_class,
				decription_class=description_class
			)

		metadata = {}
		for description in descriptions:
			if description.get_attribute("data-filmname") != description.text: continue
			metadata[description.text.replace(":","")] = {
				"data-filmname": description.get_attribute("data-filmname").replace(":",""),
				"data-year":     description.get_attribute("data-year"),
				"data-imdb":     description.get_attribute("data-imdb").split(": ")[1],
				"data-duration": description.get_attribute("data-duration"),
				"data-country":  description.get_attribute("data-country"),
				"data-genre":    description.get_attribute("data-genre"),
				"data-descript": description.get_attribute("data-descript"),
				"img":           description.find_element_by_tag_name("img").get_attribute("src")
			}
		return results, metadata

	def get_metadata_from_video(self, url):
		filmname = self.driver.find_element(
			By.XPATH, "//*[@id=\"info\"]/div[1]/div[1]/h1"
		).text

		metadata = {}

		description = (
			self.driver.find_elements(By.CLASS_NAME, "_skQummZWZxE") + \
			self.driver.find_elements(By.CLASS_NAME, "_snsNGwwUUBn") + \
			self.driver.find_elements(
				By.XPATH, "/html/body/main/div/div/section/div[5]/div/box/div/div/div/div[3]"
			)
		)

		metadata[filmname] = {
			"data-filmname": filmname,
			"data-year":     description[0].text.split("\n")[1],
			"data-imdb":     description[1].text.split("\n")[1],
			"data-duration": description[3].text.split("\n")[1],
			"data-country":  description[8].text.split(": ")[1],
			"data-genre":    description[6].text.split(": ")[1],
			"data-descript": self.driver.find_element(
							 	 By.CLASS_NAME, "_snmrSkaJSTK").text.split("\n")[1],
			"img":           description[-1].get_attribute("src")
		}

		if not metadata[filmname]["img"]:
			metadata[filmname]["img"] = \
				"https://upload.wikimedia.org/wikipedia/commons/a/af/Question_mark.png"
		return metadata

	def wait_until_element(self, stratagy, locator, timeout=10):
		wait = WebDriverWait(self.driver, timeout)
		element = wait.until(
			EC.presence_of_element_located(
				(
					stratagy, locator
				)
			)
		)
		return element

	def open_link(self, url):
		self.driver.get(url)
		# The following code only runs when the adblock is still initializing from the first launch
		if self.first_launch:
			# Searches for any ads on the site
			element = self.driver.find_elements(
				By.XPATH,
				"//*[@id=\"container-b530c7d909bb9eb21c76642999b355b4\"]/div[2]/div[5]/div/div[3]"
			)
			if element:  # If any ads were found, refresh the page and run the ad check again
				time.sleep(0.5)
				self.driver.refresh()
				self.open_link(url)
			self.first_launch = False

	def current_url(self):
		return self.driver.current_url

	def close(self):
		self.driver.close()

	def get_results_from_search(self, element_class="item_hd", decription_class="_smQamBQsETb"):
		elements = self.driver.find_elements_by_class_name(element_class)
		description = self.driver.find_elements_by_class_name(decription_class)  # _skQummZWZxE
		return elements, description

	def screenshot_captcha(self, captcha_element, filename="captcha.png"):
		self.driver.save_screenshot(filename)
		# self.driver.save_screenshot("full_page.png")
		location = captcha_element.location
		location["y_off"] = 50
		location["x_off"] = 120
		return crop.crop(filename, location, cfg.executable)

	def check_captcha(self):
		# Myles
		# Liam
		try:
			captcha_image = self.wait_until_element(
				By.XPATH,
				"//*[@id=\"checkcapchamodelyii-captcha-image\"]",
				timeout=1.5
			)
			captcha_input = self.driver.find_element(By.XPATH, "//*[@id=\"checkcapchamodelyii-captcha\"]")
			captcha_submit = self.driver.find_element(By.XPATH, "//*[@id=\"player-captcha\"]/div[3]/div/div")
		except TimeoutException:
			return None, None, None
		if captcha_image:
			print("DEBUG: Captcha!")
			log("Captcha! Solve using the command:\n```beta solve <captcha_solution>```")

		return captcha_image, captcha_input, captcha_submit

	def run_captcha_functions(self):
		captcha_image, captcha_input, captcha_submit = self.check_captcha()
		if captcha_image:
			time.sleep(0.25)
			self.screenshot_captcha(captcha_image)

			# log("DEBUG--file=captcha.png")
			# solved_captcha = check_for_captcha_solve(timeout=1)
			solved_captcha = False

			if solved_captcha:
				captcha_input.send_keys(solved_captcha)
				captcha_submit.click()

	def get_download_link(self, source_url, timeout=10):
		movie = "watch-tv-show" not in source_url
		# Link is a movie
		if movie:
			source_url = source_url.split(".html")[0] + (".html" if ".html" in source_url else "")
			if not source_url.endswith("-online-for-free.html"):
				# https://gomovies-online.cam/watch-film/the-godfather/axTk1vHi/7i7waSMV
				# https://gomovies-online.cam/watch-film/the-godfather/axTk1vHi/7i7waSMV.html-online-for-free.html
				# https://gomovies-online.cam/watch-film/the-godfather/axTk1vHi/7i7waSMV-online-for-free.html
				source_url += "-online-for-free.html"
			source_url_list = [source_url]
		# Link is a TV show season
		elif not source_url.endswith(".html"):
			self.open_link(source_url)
			source_url_list = self.driver.find_elements(By.XPATH, "//*[@class=\"_sXFMWEIryHd \"]")
			for index, source_url in enumerate(source_url_list):
				source_url_list[index] = source_url.get_attribute("href")
		# Link is a TV show episode
		else:
			source_url = source_url.split(".html")[0] + ".html"
			if not source_url.endswith("-online-for-free.html"):
				source_url += "-online-for-free.html"
			source_url_list = [source_url]

		download_queue = []
		for url in source_url_list:
			if not url.endswith("-online-for-free.html"):
				continue

			self.open_link(url)
			if self.run_captcha_functions(): self.get_download_link(url, timeout)
			metadata = self.get_metadata_from_video(url)  # Works for movies and TV
			target_url = self.wait_until_element(
				By.TAG_NAME, "video", timeout
			).get_attribute("src")

			self.driver.execute_script(
				"videos = document.querySelectorAll(\"video\"); for(video of videos) {video.pause()}"
			)

			print(target_url)
			download_queue.append((target_url,metadata,self.author))
			# TODO: write all of the download links to a list so they can be downloaded in sequential order later (maybe return the list?)
		return download_queue

	# '''Demitri's Holy Contribution'''
	# def get_movie(self, name):
	# 	self.driver.get_link_by_partial_text("").click()
	# 	self.driver.find_element_by_tag_name("input").text()

	def download_first_from_search(self, search_query):
		start_time = time.time()
		search_results, metadata = self.search(
			"https://gomovies-online.cam/search/" + \
			"-".join(search_query.split())
		)
		if search_results:
			search_time_elapsed = round(time.time()-start_time,2)
			print(f"Finished scraping {len(search_results)} results in {search_time_elapsed} seconds!")
			source_url = search_results[0].get_attribute("href")
			download_queue = self.get_download_link(
				source_url + ("-online-for-free.html" if "watch-tv-show" not in source_url else "")
			)  # [(x,y,z),(x,y,z),(x,y,z),...(x,y,z)]
			print("Link found." if len(download_queue) == 1 else f"{len(download_queue)} links found.")
		else:
			print("Error: No search results found!")
		print(f"Finished all scraping in {round(time.time()-start_time,2)} seconds!")
		return download_queue  # [(url,metadata,author)]

	def run(self, search_query):
		download_queue = self.download_first_from_search(search_query)[0]
		return download_queue


def check_for_captcha_solve(timeout=100):
	if __name__ == "__main__":
		media.write_file("captcha.txt", input("Solve the captcha:\n> "))

	filename = "captcha.txt"
	for half_second in range(timeout*2):
		time.sleep(0.5)
		if os.path.isfile(filename):
			solved_captcha = media.read_file(filename)[0]
			media.remove_file(filename)
			return solved_captcha
	log(f"Captcha was not solved withing {timeout} seconds.\nAborting download.", silent=False)
	return False

def error(e):
	''' Code by Confused Cottonmouth - Jan 13 2021 '''
	exc_type, exc_obj, exc_tb = sys.exc_info()
	filename = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	return f"```javascript\nException type:  {exc_type}\nFile name:       {filename}\nLine Number:     {exc_tb.tb_lineno}\nException data:  {e}```"


if __name__ == "__main__":
	scraper = Scraper(minimize=False)
	while True:
		query = input("Enter a Title to search for:\n> ")
		if query:
			scraper.run(query)
		else:
			break
	scraper.close()

# The criminal I've been chasing is wearing my shoes.
