def microcenter(self, url):
		self.open_link(url)
		items = {}
		results = self.driver.find_elements(
			By.XPATH, "//*[@class=\"product_wrapper\"]"
		)
		for result in results:
			# Normal advertised Sale Price
			try: price = result.find_element(
					By.XPATH, "./div[2]/div/div[2]/div[1]/span").text
			except NoSuchElementException: price = False

			# Price after mail-in Rebate
			try: rebate_price = result.find_element(
					By.XPATH, "./div[2]/div/div[2]/div[2]").text
			except NoSuchElementException: rebate_price = False

			# Price for Open Boxed items
			try: clearance_price = result.find_element(
					By.XPATH, "./div[2]/div/div[2]/div[3]/span").text
			except NoSuchElementException: clearance_price = False

			# Product SKU
			sku = result.find_element(
					By.XPATH, "./div[2]/div/div[1]/p").text[5:]
			# //*[@id="pwrapper_1"]/div[2]/div/div[1]/p

			print(f"SKU: {sku}")
			print(f"Price:           {price}")
			print(f"Rebate Price:    {rebate_price if rebate_price else False}")
			print(f"Clearance Price: {clearance_price}\n")

			items[sku] = {
				"price": price,
				"rebate_price": rebate_price,
				"clearance_price": clearance_price,
			}

		return items

	def best_buy(self, url):
		self.open_link(url)
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		items = {}
		results = self.driver.find_elements(
			By.XPATH, "//*[@class=\"sku-item\"]"
		)
		for result in results:
			# Normal advertised Sale Price
			try: price = result.find_element(
					By.XPATH, "./div/div/div/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/div/div[2]/div/div[1]/div/span[1]").text
			except NoSuchElementException: price = False

			# Price after mail-in Rebate
			try: rebate_price = result.find_element(
					By.XPATH, "W.I.P.").text
			except NoSuchElementException: rebate_price = False

			# Price for Open Boxed items
			try: clearance_price = result.find_element(
					By.XPATH, "./div/div/div/div/div/div[2]/div[2]/div[5]/div/div/div/div/div/div/div/div/a/span[2]").text.split("from ")[1]
			except NoSuchElementException: clearance_price = False
			except IndexError: clearance_price = False

			# Product SKU
			sku = result.find_element(
					By.XPATH, "./div/div/div/div/div/div[2]/div[1]/div[3]/div[1]/div[2]/span[2]").text

			# Product Name
			name = result.find_element(
					By.XPATH, "./div/div/div/div/div/div[2]/div[1]/div[2]/div/h4/a").text

			# Product URL
			url = result.find_element(
					By.XPATH, "./div/div/div/div/div/div[2]/div[1]/div[2]/div/h4/a").get_attribute("href")

			print(f"Name: {name}")
			print(f"SKU:  {sku}")
			print(f"Price:           {price}")
			print(f"Rebate Price:    {rebate_price if rebate_price else False}")
			print(f"Clearance Price: {clearance_price}")
			print(f"URL: {url}\n")

			items[sku] = {
				"price": price,
				"rebate_price": rebate_price,
				"clearance_price": clearance_price,
			}

	def amazon(self, url):
		self.open_link(url)
		self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		time.sleep(3)
		items = {}
		results = self.driver.find_elements(
			By.XPATH, "//div[@class=\"a-section a-spacing-none\"]"
		)
		# /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/span/div

		# Product Name
		names = self.driver.find_elements(
				By.XPATH, "//h2[@class=\"a-size-mini a-spacing-none a-color-base s-line-clamp-2\"]")

		# Product URL
		urls = self.driver.find_elements(
				By.XPATH, "//h2[@class=\"a-size-mini a-spacing-none a-color-base s-line-clamp-2\"]/a")

		for index, result in enumerate(results):
			# Product SKU
			sku = result.get_attribute("data-asin")
			# /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[3]
			name = names[index].text
			url  = urls[index].get_attribute("href")

			#                                                                ./div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a/span
			# /html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[3]/div/span/div/div/div[2]/div[2]/div/div/div[1]/h2/a/span



			print(f"Name: {name}")
			print(f"SKU:  {sku}")
			# print(f"Price:           {price}")
			# print(f"Rebate Price:    {rebate_price if rebate_price else False}")
			# print(f"Clearance Price: {clearance_price}")
			print(f"URL: {url}\n")
