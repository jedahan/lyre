import numpy as np
import cv2
from matplotlib import pyplot as plt

orb = cv2.ORB()

needle = cv2.imread('needle-stripped.png',0)   # needle
keypoint = orb.detect(needle, None)
keypoint, description = orb.compute(needle, keypoint)

from os import listdir
from os.path import isfile, join
files = [ f for f in listdir('haystack') if isfile(join('haystack',f)) ]

descriptions = []
keypoints = []

for file in files:
  haystack = cv2.imread(file,0) # haystack
  h_keypoint, h_description = orb.compute(haystack, keypoint)
  keypoints.append(h_keypoint)
  descriptions.append(h_description)

print keypoint

print description

# FLANN parameters
FLANN_INDEX_KDTREE = 0
FLANN_INDEX_LSH    = 6

index_params= dict(algorithm = FLANN_INDEX_LSH,
                   table_number = 6, # 12
                   key_size = 12,     # 20
                   multi_probe_level = 1) #2
search_params = dict(checks=50)   # or pass empty dictionary

flann = cv2.FlannBasedMatcher(index_params,search_params)

best_match_size = 0
best_match_index = -1
match_index = 0
best_matches = 0

for desc in descriptions:
  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
  matches = bf.match(desc,description)
  matches = sorted(matches, key = lambda x:x.distance)

  print "match size is ", len(matches)
  if  len(matches) > best_match_size:
    print 'FOUND BEETTER MATCH'
    best_match_size = len(matches)
    best_match_index = match_index
    best_matches = matches

  match_index += 1

best_match_images = cv2.imread("haystack/"+files[best_match_index])
print "best match is ", files[best_match_index]
#match = cv2.drawMatchesKnn(needle,keypoint,best_match_images,keypoints[best_match_index],best_matches,None,**draw_params)

# cv2 is little-endian (BGR), while matplotlib is big-endian (RGB)
plt.imshow(best_match_images[:,:,::-1], interpolation = 'bicubic')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
