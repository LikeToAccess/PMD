# -*- coding: utf-8 -*-
# filename          : microcenter.py
# description       : Get RAM for LOW prices
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 08-06-2021
# version           : v1.0
# usage             : python microcenter.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
from scraper import Scraper


scraper = Scraper(minimize=False)
url = "https://www.microcenter.com/search/search_results.aspx?N=4294966965+4294818366+4294809583+4294816624&Ntt=&prt=&sku_list=&Ntx=&Ntk=all&Nr="
# url = "https://www.microcenter.com/category/4294966928/air-water-cooling"


if __name__ == "__main__":
	scraper.microcenter(url)
	scraper.close()
	quit()
