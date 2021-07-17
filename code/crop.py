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


def crop(img, loc):
	print(loc)
	image = cv2.imread(img)
	ROI = image[loc["y"]:loc["y"]+50, loc["x"]:loc["x"]+120]
	img = img.split(".")[0]
	cv2.imwrite(img, ROI)
	return img


if __name__ == "__main__":
	crop("captcha.png", {"x": 396, "y": 464})
