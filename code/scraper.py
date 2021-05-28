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
import media
from media import log
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class Scraper:
	def __init__(self, link):
		self.link = link
		options = Options()
		options.add_argument("--headless")
		executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
		print(f"DEBUG: {executable}")
		self.driver = webdriver.Chrome(executable_path=os.path.abspath(executable), options=options)
		self.driver.get(self.link)

	def check_captcha(self, xpath="//*[@id=\"checkcapchamodelyii-captcha-image\"]", attr="src"):
		try:
			captcha = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,xpath)))
			captcha = self.driver.find_element_by_xpath(xpath)
			captcha = captcha.get_attribute(attr)
			print(f"DEBUG: Captcha, {captcha}")
		except TimeoutException:
			print("DEBUG: No captcha")
			captcha = False
		if captcha:
			log("Captcha! Please solve using the command: ```!solve <captcha_solution>```\nREMIND IAN TO FIX THIS --> please don't mess up or the download will fail.")
			log(captcha)
			filename = "solved_captcha.txt"
			solved_captcha = False
			while not solved_captcha:
				sleep(1)
				if os.path.isfile(filename):
					solved_captcha = media.read_file(filename)
					media.remove_file(filename)
					print(f"DEBUG: Solved captcha, {solved_captcha}")
				print(f"DEBUG: Checking for {filename}")
			# MAKE SELENIUM SOLVE THE CPAATCHA

		return captcha

	def run(self, xpath="//*[@id=\"_skqeqEJBSrS\"]/div[2]/video", attr="src"):
		print("WEB SCRAPING")
		log("Waiting on web scraper (up to 35 seconds).")
		self.check_captcha()
		print("DEBUG: Finished check_captcha function")
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
	scraper = Scraper("https://gomovies-online.cam/watch-film/wrath-of-man/CCmkfFgE/kp6jEoRd")
	print(scraper.run())
