import click
import numpy as np
import cv2
from matplotlib import pyplot as plt


@click.command()
@click.argument('images', nargs=-1)
def describe(images):
  """print out the keypoints and description for IMAGE"""
  for image in images:
    needle = cv2.imread(image, 0)
    orb = cv2.ORB()
    keypoints, description = orb.detectAndCompute(needle, None)
    print(keypoints)
    print(description)
    return keypoints, description

@cli.command()
@click.argument('images')
def save(images):
  """save IMAGE keypoints and description to the database"""
  connect_to_db()
  keypoints, description = describe(image)
  artwork = {
    "keypoints": keypoints,
    "description": description,
    "path": image,
    "date": datetime.datetime.utcnow()
  }
  artwork_id = db.insert(artwork)
  print(artwork_id)

@cli.command()
@click.argument('image')
def find(image):
  """use IMAGE to search for similar images that are in the db"""
  keypoint, description = describe(image)
  connect_to_db()
  # load keypoints, descriptions from mongodb

  bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

  best_match_size = float("inf")
  best_match_index = -1
  match_index = 0
  best_matches = 0

  for desc in descriptions:
    matches = bf.match(desc,description)
    matches = sorted(matches, key = lambda x:x.distance)
    if len(matches) > 0:
      match_size = sum(x.distance for x in matches[:10])

      print "match size is ", match_size
      if  match_size < best_match_size:
        best_match_size = match_size
        best_match_index = match_index
        best_matches = matches

    match_index += 1

  needle_color = cv2.imread('needle-stripped.png')[:,:,::-1]   # needle
  best_match_image = cv2.imread("haystack/"+files[best_match_index])
  print "best match is ", files[best_match_index]

  # Draw first 10 matches.
  outImg = cv2.imread("output/outImg.png")
  match = cv2.drawMatches(needle_color,keypoint,best_match_image[:,:,::-1],keypoints[best_match_index],best_matches[-20:],outImg, flags=6)

  plt.imshow(match),plt.show()
  return

def connect_to_db():
  from pymongo import MongoClient
  client = MongoClient()
  db = client.images

if __name__ == '__main__':
    describe()
