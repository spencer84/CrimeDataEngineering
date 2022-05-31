import requests
import json
import numpy as np
import sqlite3
import datetime


def find_most_recent_month():
    """Returns the most recent month with data available"""
    most_recent_month = datetime.datetime.today()
    # Use a polygon surrounding Bexhill as a test point to see what data available
    results = requests.post(url,
                            params={
                                'poly': '50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691'
                                , 'date': most_recent_month.strftime("%Y-%m")})
    while results.status_code == 404:
        most_recent_month = most_recent_month - datetime.timedelta(days=28)
        results = requests.post(url,
                                params={
                                    'poly': '50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691'
                                    , 'date': most_recent_month.strftime("%Y-%m")})
    while len(results.json()) == 0:
        most_recent_month =  most_recent_month - datetime.timedelta(days= 28)
        results = requests.post(url,
                                params={
                                    'poly': '50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691'
                                    , 'date': most_recent_month.strftime("%Y-%m")})
    return most_recent_month.strftime("%Y-%m")

month = find_most_recent_month()

def json_to_df(json_data, cur, area,month):
    for i in json_data:
        lat = i['location']['latitude']
        lng = i['location']['longitude']
        type = i['category']
        street = i['location']['street']['name']
        if 'On or near ' in street:
            street.replace('On or near ','')
        vals = str(tuple(area,month,lng, lat, street, type))
        query = "Insert into crime (police_area, month, lng, lat, street, type) VALUES "+ vals


url = 'https://data.police.uk/api/crimes-street/all-crime'

# Update unique lat long pairings

# Connect to the database
conn = sqlite3.connect('crime.db')

cur = conn.cursor()

# Select distinct lat long pairings

query = "select distinct lat, lng, police_area from crime;"

cur.execute(query)

unique_locations = cur.fetchall()

# Iterate through all combinations performing a GET request
# then load json results back into the database
for i in unique_locations[:5]:
    results = requests.get(url, params={'lat': i[0], 'lng': i[1], 'date': month})


# Read in Geojson file to get the coordinates of each police area
geo = json.load(open('Police_Force_Areas_(December_2020)_EW_BFE.geojson'))
test = geo['features'][0]['geometry']['coordinates']
results = requests.post(url,
                        params={'poly': '50.864508,0.423318:50.868408,0.503656:50.840232,0.507775:50.831993,0.424691',
                                'date': '2020-01'})
full_england = requests.get(url, params={'poly': '56,-6:56,2.6:49.8,2.6:49.8,-6', 'date': '2020-01'})


class BoundingBox:
    def __init__(self, p1, p2, p3, p4, split):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4
        self.next_split = split

    def generate_poly(self):
        # Create a string to fit the API requirements for a polygon
        t1 = ','.join([str(x) for x in self.p1])
        t2 = ','.join([str(x) for x in self.p2])
        t3 = ','.join([str(x) for x in self.p3])
        t4 = ','.join([str(x) for x in self.p4])
        return t1 + ':' + t2 + ':' + t3 + ':' + t4


def h_split(bb):
    # Split the bounding box horizontally and return two new boxes
    bb1 = BoundingBox(bb.p1.copy(), bb.p2, bb.p3, bb.p4, 'v')
    mid_point = np.mean([bb1.p1[0], bb1.p4[0]])
    bb1.p4[0] = mid_point
    bb1.p3[0] = mid_point
    bb2 = BoundingBox(bb.p1, bb.p2, bb.p3, bb.p4, 'v')
    bb2.p1[0] = mid_point
    bb2.p2[0] = mid_point
    bb1.next_split = 'v'
    bb2.next_split = 'v'
    return bb1, bb2


def v_split(bb):
    # Split the bounding box vertically and return two new boxes
    bb1 = BoundingBox(bb)
    mid_point = np.mean([bb1.p1[1], bb1.p2[1]])
    bb1.p2[1] = mid_point
    bb1.p3[1] = mid_point
    bb2 = BoundingBox(bb.p1, bb.p2, bb.p3, bb.p4, 'h')
    bb2.p1[1] = mid_point
    bb2.p4[1] = mid_point
    bb1.next_split = 'h'
    bb2.next_split = 'h'
    return bb1, bb2


def split(bb):
    if bb.next_split == 'h':
        return h_split(bb)
    elif bb.next_split == 'v':
        return v_split(bb)


full_england = BoundingBox([56, -6], [56, 2.6], [49.8, 2.6], [49.8, -6], 'h')


def divide_and_conquer(full_england):
    # Create
    areas = [full_england]
    url = 'https://data.police.uk/api/crimes-street/all-crime'
    while len(areas) > 0:
        for i in areas:
            poly = i.generate_poly()
            areas.remove(i)
            print(areas)
            results = requests.get(url, params={'poly': poly, 'date': '2020-01'})
            if results.status_code == 503:  # Too many results
                print("Too many results...splitting polygon")
                splits = i.split()
                for split in splits:
                    areas.append(split)
                areas
            elif results.status_code == 200:
                json_to_df(results)
            else:
                print(f"Error! Status code {results.status_code}")


divide_and_conquer(full_england)
