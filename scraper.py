import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Scraper:
	def __init__(self, link):
		self.link = link
		options = Options()
		options.add_argument("--headless")
		executable = "chromedriver.exe" if os.name == "nt" else "chromedriver"
		print(executable)
		self.driver = webdriver.Chrome(executable_path=os.path.abspath(executable), options=options)
		self.driver.get(self.link)

	def run(self, xpath="//*[@id=\"_skqeqEJBSrS\"]/div[2]/video", attr="src"):
		element = WebDriverWait(self.driver, 30).until(EC.visibility_of_element_located((By.XPATH,xpath)))
		element = self.driver.find_element_by_xpath(xpath)
		data = element.get_attribute(attr)
		while len(data) < 100:
			print("DEBUG: No data!")
			self.driver.refresh()
			data = self.run(xpath, attr)
		self.driver.quit()
		return data


if __name__ == "__main__":
	link = "https://gomovies-online.cam/watch-film/wrath-of-man/CCmkfFgE/kp6jEoRd"
	scraper = Scraper(link)
	print(scraper.run())
