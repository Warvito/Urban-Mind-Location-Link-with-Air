"""Script to find the nearest gridpoints (with air pollution measures) to the Urban Mind dataset.

In order to find the nearest point, first we remove all gridpoints with missing values. Then we convert the OSGB 1936
British National Grid measures to the WGS 84 (GPS) latitude and longitude values. Finally, we compute the separation
between the coordinates (using the great-circle distance, https://docs.astropy.org/en/stable/coordinates/matchsep.html).
We used astropy library (instead geopy, for example) due to its efficient to calculate the distance. A maximum distance
of 3 km is used to assign the air pollution measures

Refs:
https://gist.github.com/amercader/927079/caa63f49d1ff36f0489f2e11cb695deb06d5b6c2
https://stackoverflow.com/questions/50275057/how-to-use-vectorization-with-numpy-arrays-to-calculate-geodesic-distance-using
https://gis.stackexchange.com/questions/84885/whats-the-difference-between-vincenty-and-great-circle-distance-calculations
https://stackoverflow.com/questions/45134554/finding-closest-point
"""
from pathlib import Path

from astropy.units import Quantity
from astropy.coordinates import SkyCoord, EarthLocation
from astropy.constants import R_earth
from astropy import units as u
import numpy as np
import pandas as pd
import pyproj

PROJECT_ROOT = Path.cwd()


def main():
    """Assign the air pollution measures to the Urban Mind dataset."""
    # -------------------------------------------------------------------------------------------
    air_pollution_map_path = PROJECT_ROOT / 'data' / 'mappm252017g.csv'
    urban_mind_path = PROJECT_ROOT / 'data' / 'Urban Mind UK Clipped.csv'

    maximal_distance = 3  # kilometers
    # -------------------------------------------------------------------------------------------
    output_dir = PROJECT_ROOT / 'outputs'
    output_dir.mkdir(exist_ok=True)

    urban_mind_df = pd.read_csv(urban_mind_path)
    air_pollution_map_df = pd.read_csv(air_pollution_map_path, skiprows=5)

    air_pollution_map_df = air_pollution_map_df[air_pollution_map_df['pm252017g'] != 'MISSING']

    # -------------------------------------------------------------------------------------------
    bng = pyproj.Proj(init='epsg:27700')  # British National Grid
    wgs84 = pyproj.Proj(init='epsg:4326')  # WGS84 (Lat/Lon)

    air_pollution_map_df['longitude'], air_pollution_map_df['latitude'] = \
        pyproj.transform(bng, wgs84, air_pollution_map_df['x'].values, air_pollution_map_df['y'].values)

    # -------------------------------------------------------------------------------------------
    urban_mind_df['pm252017g'] = np.nan
    for urban_mind_index, urban_mind_row in urban_mind_df.iterrows():
        print(urban_mind_index)
        lon1 = Quantity(air_pollution_map_df['longitude'].values, unit='deg')
        lat1 = Quantity(air_pollution_map_df['latitude'].values, unit='deg')
        lon2 = Quantity(urban_mind_row['startlongi'], unit='deg')
        lat2 = Quantity(urban_mind_row['startlatit'], unit='deg')

        pts1 = SkyCoord(EarthLocation.from_geodetic(lon1, lat1, height=R_earth).itrs, frame='itrs')
        pts2 = SkyCoord(EarthLocation.from_geodetic(lon2, lat2, height=R_earth).itrs, frame='itrs')

        dist_in_degree = pts2.separation(pts1)

        dist = np.deg2rad(dist_in_degree) * R_earth / u.rad
        dist = np.asarray(dist) / 1000  # transform to kilometers

        if np.min(dist) <= maximal_distance:
            nearest_point = air_pollution_map_df.iloc[np.argmin(dist)]

            urban_mind_df.iloc[urban_mind_index,
                               urban_mind_df.columns.get_loc('pm252017g')] = nearest_point['pm252017g']

    urban_mind_df.to_csv(output_dir / 'urban_mind_w_air_pollution.csv', index=False)


if __name__ == "__main__":
    main()
