import requests
import json

url = 'https://data.police.uk/api/crimes-street/all-crime'

# Read in Geojson file to get the coordinates of each police area
geo = json.load(open('Police_Force_Areas_(December_2020)_EW_BFE.geojson'))
test = geo['features'][0]['geometry']['coordinates']
results = requests.post(url, params= {'poly':'50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691','date':'2020-01'})

def get_police_area(geo_feature):
    props = geo_feature['properties']
    return props['PFA20NM']
def get_current_month():

def geojson_to_string(coordinates):
    """Quick function to take geocoordinates from a geojson file to the format required
    """
    text = ''
    for i in coordinates:
        val = str(i)
        if text == '': # Check if this is first value; can't lead with ':
            val = val.replace('[', '')
        else:
            val = val.replace('[', ':')
        val = val.replace(']', ':')
        text += val
    return text[:-1] # Remove last colon