# -*- coding: utf-8 -*-
# filename          : crop.py
# description       : Crop images
# author            : LikeToAccess
# email             : liketoaccess@protonmail.com
# date              : 06-07-2021
# version           : v1.0
# usage             : python crop.py
# notes             :
# license           : MIT
# py version        : 3.8.2 (must run on 3.6 or higher)
#==============================================================================
import cv2

def crop(img, loc, executable):
	print(loc)
	image = cv2.imread(img)
	if ".exe" not in executable:
		loc["y"]     = loc["y"]     * 2
		loc["x"]     = loc["x"]     * 2
		loc["y_off"] = loc["y_off"] * 2
		loc["x_off"] = loc["x_off"] * 2
	ROI = image[
		loc["y"]:loc["y"]+loc["y_off"],
		loc["x"]:loc["x"]+loc["x_off"]
	]
	try:
		cv2.imwrite(img, ROI)
	except cv2.error:
		return crop(img, loc, executable)
	return img

if __name__ == "__main__":
	crop("captcha.png", {'x': 540, 'y': 462, 'x_off': 120, 'y_off': 50}, "driver")
