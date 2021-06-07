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
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException


class Scraper:
	def __init__(self, link):
		self.link = link
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
		self.driver.get(self.link)
		sleep(1)
		window_name = self.driver.window_handles[1]
		self.driver.switch_to.window(window_name=window_name)
		self.driver.close()
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
		start_time = time()
		try:
			captcha_element = WebDriverWait(self.driver,5).until(EC.visibility_of_element_located((By.XPATH,xpath)))
			captcha_element = self.driver.find_element_by_xpath(xpath)
			captcha = captcha_element.get_attribute(attr)
			filename = self.screenshot_captcha(captcha_element)

			# action_chains = ActionChains(self.driver)
			# action_chains.move_to_element(captcha_element).context_click().send_keys(Keys.ARROW_DOWN).send_keys(Keys.ARROW_DOWN).send_keys(Keys.ENTER).perform()
			# with open("captcha.png", "wb") as file:
			# 	file.write()
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
				while not solved_captcha and (time() - start_time) < 60:
					sleep(1)
					# print(f"DEBUG: Checking for {filename}")
					if os.path.isfile(filename):
						solved_captcha = media.read_file(filename)[0]
						media.remove_file(filename)
						print(f"DEBUG: Solved captcha, {solved_captcha}, {not solved_captcha}/{(time() - start_time) < 90}")
			else:
				solved_captcha = input("Enter the solved captcha:\n> ")
			if solved_captcha:
				self.solve_captcha(solved_captcha)
				self.submit_captcha()
				# self.run()

		return captcha

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
	scraper = Scraper("https://gomovies-online.cam/watch-film/wrath-of-man/CCmkfFgE/kp6jEoRd-online-for-free.html")
	print(scraper.run())
