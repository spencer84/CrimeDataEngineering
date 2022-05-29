import requests

url = 'https://data.police.uk/api/crimes-street/all-crime'

results = requests.get(url, params= {'poly':'50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691','date':'2020-01'})