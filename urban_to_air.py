"""
https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
https://gis.stackexchange.com/questions/84885/whats-the-difference-between-vincenty-and-great-circle-distance-calculations
"""
from pathlib import Path

import geopy.distance
import pandas as pd
import pyproj


PROJECT_ROOT = Path.cwd()



def main():
    """"""
    air_map_path = PROJECT_ROOT / 'data' / 'mappm252017g.csv'
    urban_mind_path = PROJECT_ROOT / 'data' / 'Urban Mind UK Clipped.csv'

    urban_mind_df = pd.read_csv(urban_mind_path)
    air_map_df = pd.read_csv(air_map_path, skiprows=5)

    air_map_df['latitude'] =
    latitude = urban_mind_df['startlatit']
    longitude = urban_mind_df['startlongi']

    bng = pyproj.Proj(init='epsg:27700')
    wgs84 = pyproj.Proj(init='epsg:4326')

    lat_list = []
    for x, y in zip(air_map_df['x'], air_map_df['y']):
        lat, lon = pyproj.transform(bng, wgs84, x, y)




if __name__ == "__main__":
    main()





import datetime
from geopy.distance import great_circle
from geopy.distance import vincenty
p1 = (31.8300167,35.0662833)
p2 = (31.83,35.0708167)

NUM_TESTS = 100000
for strategy in vincenty, great_circle:
    before = datetime.datetime.now()
    for i in range(NUM_TESTS):
        d=strategy(p1, p2).meters
    after = datetime.datetime.now()
    duration = after-before
    print "%-40s: Total %s, (%s per calculation)" % (strategy, duration, duration/NUM_TESTS)


import geopy.distance

coords_1 = (52.2296756, 21.0122287)
coords_2 = (52.406374, 16.9251681)

print geopy.distance.vincenty(coords_1, coords_2).km


>>> from geopy.distance import great_circle
>>> from geopy.distance import vincenty
>>> p1 = (31.8300167,35.0662833) # (lat, lon) - https://goo.gl/maps/TQwDd
>>> p2 = (31.8300000,35.0708167) # (lat, lon) - https://goo.gl/maps/lHrrg
>>> vincenty(p1, p2).meters
429.16765838976664
>>> great_circle(p3, p4).meters
428.4088367903001