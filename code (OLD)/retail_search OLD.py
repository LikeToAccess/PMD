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


scraper = Scraper(minimize=True)
url = {
	"amazon": "https://www.amazon.com/s?k=OLED65C1PUB&i=electronics&rh=n%3A6463520011%2Cp_n_size_browse-bin%3A1232883011%2Cp_n_feature_nine_browse-bin%3A23478599011%2Cp_89%3ALG%2Cp_n_feature_six_browse-bin%3A2807397011&dc&qid=1633101031&rnid=2807395011&ref=sr_nr_p_n_feature_six_browse-bin_2",
	"best_buy": "https://www.bestbuy.com/site/searchpage.jsp?id=pcat17071&qp=brand_facet%3DBrand~LG%5Ecategory_facet%3DAll%20Flat-Screen%20TVs~abcat0101001%5Efeatures_facet%3DFeatures~Dolby%20Atmos%5Eparent_tvscreensizeplus_facet%3DTV%20Screen%20Size~65%22%20-%2074%22%5Evoiceassistant_facet%3DVoice%20Assistant%20Built-in~Google%20Assistant&st=6453312"
}


if __name__ == "__main__":
	# scraper.microcenter(url)
	scraper.best_buy(url["best_buy"])
	scraper.amazon(url["amazon"])
	scraper.close()
	quit()
