"""
brute force method O(N**2) ~ 350 h

KD-tree O(N*log(N)) ~


https://stackoverflow.com/questions/45127141/find-the-nearest-point-in-distance-for-all-the-points-in-the-dataset-python

https://codereview.stackexchange.com/questions/28207/finding-the-closest-point-to-a-list-of-points
https://gis.stackexchange.com/questions/84885/whats-the-difference-between-vincenty-and-great-circle-distance-calculations

https://stackoverflow.com/questions/50275057/how-to-use-vectorization-with-numpy-arrays-to-calculate-geodesic-distance-using

https://stackoverflow.com/questions/45134554/finding-closest-point
"""
from pathlib import Path
import time

from geopy.distance import great_circle, geodesic
import pandas as pd
import numpy as np
import pyproj

from astropy.units import Quantity
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.constants import R_earth
from astropy import units as u
import numpy as np

PROJECT_ROOT = Path.cwd()


def main():
    """"""
    air_map_path = PROJECT_ROOT / 'data' / 'mappm252017g.csv'
    urban_mind_path = PROJECT_ROOT / 'data' / 'Urban Mind UK Clipped.csv'

    urban_mind_df = pd.read_csv(urban_mind_path)
    air_map_df = pd.read_csv(air_map_path, skiprows=5)

    air_map_df = air_map_df[air_map_df['pm252017g'] != 'MISSING']
    #
    # latitude = urban_mind_df['startlatit']
    # longitude = urban_mind_df['startlongi']
    # TODO: Consider endlati


    bng = pyproj.Proj(init='epsg:27700')
    wgs84 = pyproj.Proj(init='epsg:4326')

    air_map_df['longitude'], air_map_df['latitude'] = pyproj.transform(bng, wgs84,
                                                                       air_map_df['x'].values, air_map_df['y'].values)

    # for urban_mind_index, urban_mind_row in urban_mind_df.iterrows():
    #     distances = np.full((len(air_map_df)), np.inf, dtype='float32')
    #     for air_map_index, air_map_row in air_map_df.iterrows():
    #         start = time.time()
    #         p1 = (urban_mind_row['startlatit'], urban_mind_row['startlongi'])
    #         p2 = (air_map_row['latitude'], air_map_row['longitude'])
    #         distances[air_map_index] = great_circle(p1, p2).km
    #         delay = time.time() - start
    #     break



    for urban_mind_index, urban_mind_row in urban_mind_df.iterrows():
        print(urban_mind_index)
        lon1 = Quantity(air_map_df['longitude'].values, unit='deg')
        lat1 = Quantity(air_map_df['latitude'].values, unit='deg')
        lon2 = Quantity(urban_mind_row['startlongi'], unit='deg')
        lat2 = Quantity(urban_mind_row['startlatit'], unit='deg')

        pts1 = SkyCoord(EarthLocation.from_geodetic(lon1, lat1, height=R_earth).itrs, frame='itrs')
        pts2 = SkyCoord(EarthLocation.from_geodetic(lon2, lat2, height=R_earth).itrs, frame='itrs')

        dist = np.deg2rad(pts2.separation(pts1)) * R_earth / u.rad

        dist = np.asarray(dist) / 1000




    import numpy as np

    lon1 = Quantity(air_map_df['longitude'].values, unit='deg')
    lat1 = Quantity(air_map_df['latitude'].values, unit='deg')
    lon2 = Quantity(urban_mind_row['startlongi'], unit='deg')
    lat2 = Quantity(urban_mind_row['startlatit'], unit='deg')

    pts1 = SkyCoord(EarthLocation.from_geodetic(lon1, lat1, height=R_earth).itrs, frame='itrs')
    pts2 = SkyCoord(EarthLocation.from_geodetic(lon2, lat2, height=R_earth).itrs, frame='itrs')

    dist = pts2.separation(pts1)



if __name__ == "__main__":
    main()





import datetime

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