import pyarrow
import os
os.environ['PYARROW'] = '1'
import polars as pl
import requests
import numpy as np
from urllib3 import request
import geopandas as gpd
import json
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString, Point


def extract_polygons(geom):
    if geom.type == 'GeometryCollection':
        # Extract all polygon parts from collection
        polygons = [part for part in geom.geoms if part.type in ['Polygon', 'MultiPolygon']]
        if polygons:
            return MultiPolygon(polygons)
        else:
            return None
    else:
        return geom

####
# First section uses geopandas to import data using the DAWA api and then 
# uses geopandas to adapt the json files 
####

danmark = requests.get("https://api.dataforsyningen.dk/landsdele?format=geojson").json()
danmark_file = '/home/jenswaaben/phd/software/adress_mapping/temp_data/danmark.json'
with open(danmark_file, mode="w") as file:
    json.dump(obj = danmark, fp= file)

dfgeo_danmark = gpd.read_file(danmark_file).explode()
dfgeo_danmark_multipoly = dfgeo_danmark.union_all()
d = {'name':'Denmark', 'index':0, 'geometry':dfgeo_danmark_multipoly}
dfgeo_danmark_oneliner = gpd.GeoDataFrame([d], 
                                          crs = "EPSG:4326")
#dfgeo_danmark_joined = dfgeo_danmark.
dfgeo_danmark_oneliner.to_file('/home/jenswaaben/phd/software/adress_mapping/data/denmark.geojson', driver = 'GeoJSON')
dfgeo_danmark_oneliner.plot("name", legend = True)
plt.savefig('/home/jenswaaben/phd/software/adress_mapping/figures/denmark.png')
plt.close()


# Now for the postnumre
postnumre_geo = requests.get("https://api.dataforsyningen.dk/postnumre?format=geojson").json()
postnumre_file = '/home/jenswaaben/phd/software/adress_mapping/temp_data/postnumre.json'
with open(postnumre_file, mode="w") as file:
    json.dump(obj = postnumre_geo, fp= file)

dfgeo_postnumre = gpd.read_file(postnumre_file).explode().explode()
postnumre_reduced = dfgeo_postnumre.intersection(dfgeo_danmark_multipoly)
dfgeo_postnumre['geometry'] = postnumre_reduced
dfgeo_postnumre.to_file('/home/jenswaaben/phd/software/adress_mapping/data/postal_codes.geojson', driver = 'GeoJSON')

# Now for the kommune
kommune_geo = requests.get("https://api.dataforsyningen.dk/kommuner?format=geojson").json()
kommune_file = '/home/jenswaaben/phd/software/adress_mapping/temp_data/kommune.json'
with open(kommune_file, mode="w") as file:
    json.dump(obj = kommune_geo, fp= file)

dfgeo_kommune = gpd.read_file(kommune_file).explode()
kommune_reduced = dfgeo_kommune.intersection(dfgeo_danmark_multipoly)
dfgeo_kommune['geometry'] = kommune_reduced
dfgeo_kommune.to_file('/home/jenswaaben/phd/software/adress_mapping/data/municipality.geojson', driver = 'GeoJSON')
dfgeo_kommune.plot('navn', legend=False)
plt.savefig("/home/jenswaaben/phd/software/adress_mapping/figures/kommuner.png")

# And lastly the regions: 
regioner_geo = requests.get("https://api.dataforsyningen.dk/regioner?format=geojson").json()
regioner_file = '/home/jenswaaben/phd/software/adress_mapping/temp_data/regioner.json'
with open(regioner_file, mode="w") as file:
    json.dump(obj = regioner_geo, fp= file)

dfgeo_regioner = gpd.read_file(regioner_file).explode()
regioner_reduced = dfgeo_regioner.intersection(dfgeo_danmark_multipoly)
dfgeo_regioner['geometry'] = regioner_reduced
dfgeo_regioner.to_file('/home/jenswaaben/phd/software/adress_mapping/data/regions.geojson', driver = 'GeoJSON')
dfgeo_regioner.plot('navn', legend=False)
plt.savefig("/home/jenswaaben/phd/software/adress_mapping/figures/regioner.png")