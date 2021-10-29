import cv2
import numpy as np
from matplotlib import pyplot as plt
import os, shutil


# cleaning workspace and copy selected images
def cleaning_and_copying(*images):
    if 'cropped' in os.listdir():
        shutil.rmtree('cropped')
    os.mkdir('cropped')
    if 'source' in os.listdir():
        shutil.rmtree('source')
    os.mkdir('source')
    if 'plots' in os.listdir():
        shutil.rmtree('plots')
    os.mkdir('plots')
    if 'thresholds' in os.listdir():
        shutil.rmtree('thresholds')
    os.mkdir('thresholds')
    for img in images:
        shutil.copy2(img, os.getcwd() + '/source')
    return 0


# function for cropping using cv2.matchTemplate
def cropping():
    dir = os.getcwd()
    template = cv2.imread('template.png', 0)
    w, h = template.shape[::-1]
    os.chdir(dir + '/source')
    images = os.listdir()
    images.sort()
    k = 10

    for imname in images:

        img = cv2.imread(imname, 0)

        method = eval('cv2.TM_CCOEFF_NORMED')
	# methods we can also use (if current one dont work): 'cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 
	# 	'cv2.TM_CCORR', 'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

        res = cv2.matchTemplate(img, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img, top_left, bottom_right, (0, 0, 0), 2)

        crp_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        cv2.imwrite(dir + '/cropped/' + str(k) + '_cropped.png', crp_img)
        k += 1
