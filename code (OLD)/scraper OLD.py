# -*- coding: utf-8 -*-
# filename          : scraper.py
# description       : Grabs movie links
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 05-27-2021
# version           : v1.0
# usage             : python scraper.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import os
from time import sleep, time
import crop
import media
import config as cfg
from media import log
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *  #TimeoutException, ElementClickInterceptedException, NoSuchElementException, NoSuchWindowException
Bannana

class Scraper:
	def __init__(self, link=False):
		self.link = link
		self.start_time = time()
		options = Options()
		files = os.listdir()
		for file in files:
			if file.endswith("crx"):
				options.add_extension(file)
		# options.add_argument("--load-extension=\"/Users/ian/Library/Application Support/Google/Chrome/Default/Extensions\"")
		# options.add_argument("--headless")
		executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
		# command = Keys.CONTROL if os.name == "nt" else Keys.COMMAND
		print(f"DEBUG: {executable}")
		self.driver = webdriver.Chrome(executable_path=os.path.abspath(executable), options=options)
		if link:
			self.driver.get(self.link)
		sleep(1)
		window_name = self.driver.window_handles[1 if link else 0]
		self.driver.switch_to.window(window_name=window_name)
		self.driver.close()
		if link:
			window_name = self.driver.window_handles[0]
			self.driver.switch_to.window(window_name=window_name)
			self.driver.refresh()
		self.headers = {"user-agent": cfg.user_agent}

	def submit_captcha(self, xpath="//*[@id=\"player-captcha\"]/div[3]/div/div"):
		button_element = self.driver.find_element_by_xpath(xpath)
		try:
			button_element.click()
			return True
		except ElementClickInterceptedException:
			print("Could not submit captcha do to ads on the site.")
		return False

	def solve_captcha(self, solved_captcha, xpath="//*[@id=\"checkcapchamodelyii-captcha\"]"):
		captcha_element = self.driver.find_element_by_xpath(xpath)
		captcha_element.send_keys(solved_captcha)

	def screenshot_captcha(self, captcha_element, filename="captcha.png"):
		self.driver.save_screenshot(filename)
		location = captcha_element.location
		return crop.crop(filename, location)

	def check_captcha(self, xpath="//*[@id=\"checkcapchamodelyii-captcha-image\"]", attr="src"):
		try:
			captcha_element = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,xpath)))
			captcha_element = self.driver.find_element_by_xpath(xpath)
			captcha = captcha_element.get_attribute(attr)
			filename = self.screenshot_captcha(captcha_element)
			print(f"DEBUG: Captcha, {captcha}")
		except TimeoutException:
			print("DEBUG: No captcha")
			captcha = False
		if captcha:
			if __name__ != "__main__":
				log("Captcha! Please solve using the command: ```!solve <captcha_solution>```\nREMIND IAN TO FIX THIS --> please don't mess up or the download will fail.")
				log(f"--file={filename}")
				filename = "solved_captcha.txt"
				solved_captcha = False
				while not solved_captcha and (time() - self.start_time) < 60:
					sleep(1)
					# print(f"DEBUG: Checking for {filename}")
					if os.path.isfile(filename):
						solved_captcha = media.read_file(filename)[0]
						media.remove_file(filename)
						print(f"DEBUG: Solved captcha, {solved_captcha}, {not solved_captcha}/{(time() - self.start_time) < 60}")
			else:
				solved_captcha = input("Enter the solved captcha:\n> ")
			if solved_captcha:
				self.solve_captcha(solved_captcha)
				self.submit_captcha()
				# self.run()

		return captcha

	def click(self, xpath):
		element = self.driver.find_element_by_xpath(xpath)
		element.click()

	# //*[@id="_sAOaKababmu"]
	# /html/body/main/div/div/section/div[1]/div/movies[1]/div/div/div/div/a
	def search(self, query):
		search_arg = "%20".join(query.split())
		self.driver.get(f"https://gomovies-online.cam/search/{search_arg}")
		try:
			self.click("/html/body/main/div/div/section/div[1]/div/movies[1]/div/div/div/div/a")
		except NoSuchElementException:
			# no results
			error = f"Search for {query} yielded no results."
			print(error)
			log(error)
			self.driver.quit()
			return False
		url = self.driver.current_url + "-online-for-free.html"
		self.driver.get(url)
		return self.run()

	def run(self, xpath="//*[@id=\"_skqeqEJBSrS\"]/div[2]/video", attr="src"):
		print("WEB SCRAPING")
		log("Waiting on web scraper (up to 35 seconds).")
		self.check_captcha()
		print("DEBUG: Finished check_captcha function")
		# self.run()
		try:
			element = WebDriverWait(self.driver,30).until(EC.visibility_of_element_located((By.XPATH,xpath)))
			element = self.driver.find_element_by_xpath(xpath)
			data = element.get_attribute(attr)
			while len(data) < 100:
				print("DEBUG: No data!")
				self.driver.refresh()
				data = self.run(xpath, attr)
			self.driver.quit()
			return data
		except TimeoutException:
			print("DEBUG: Link invalid, scraping failed.")
			return False


if __name__ == "__main__":
	movie = input("Enter a movie name:\n> ")
	scraper = Scraper("https://gomovies-online.cam")
	print(scraper.search(movie))
