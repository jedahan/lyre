#!/usr/bin/python
import cv2
img = cv2.imread('compare.jpg')

def recalculate_histograms
  for channel in [0,1,2]
    for image in images
      histograms[image.filename] = cv2.calcHist(image,channel,None,[256],[0,256])

