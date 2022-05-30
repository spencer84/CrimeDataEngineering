import requests
import json

url = 'https://data.police.uk/api/crimes-street/all-crime'

# Read in Geojson file to get the coordinates of each police area
geo = json.load(open('Police_Force_Areas_(December_2020)_EW_BFE.geojson'))

results = requests.get(url, params= {'poly':'50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691','date':'2020-01'})