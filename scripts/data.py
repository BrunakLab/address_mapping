from tkinter.ttk import Separator
import polars as pl
import pandas as pd
import numpy as np
from urllib.request import urlretrieve
import requests
from shapely.geometry import Point
import geopandas as gpd

def replace_levels(level_1, level_2, level_3): 
    return(pl.when(pl.col(level_1).is_not_null())
      .then(pl.col(level_1))
      .when(pl.col(level_1).is_null() & pl.col(level_2).is_not_null())
      .then(pl.col(level_2))
      .when(pl.col(level_1).is_null() & pl.col(level_2).is_null() & pl.col(level_3).is_not_null())
      .then(pl.col(level_3))
      .otherwise(pl.lit(None)))

# I start with organisations 
# https://statistik.medcom.dk/exports/organisations.zip
url_org = 'https://statistik.medcom.dk/exports/organisations.csv'
query_parameters = {"downloadformat": "csv"}
file_url_org = "/home/jenswaaben/phd/software/adress_mapping/temp_data/org.csv"
file_final_org = "/home/jenswaaben/phd/software/adress_mapping/data/org.csv"
np.cumsum([1,2,3])
response = requests.get(url_org, params=query_parameters)
text = response.content.decode("ISO-8859-1")

with open(file_url_org, mode="w", encoding='utf-8') as file:
    file.write(text)

temp_frame = (pl.scan_csv(file_url_org, 
            separator=';', 
            schema_overrides={'SghAfd-kode':pl.String, "Telefon":pl.String, "B_Postnummer":pl.String}, 
            truncate_ragged_lines=True)
    .select(['SOR-kode', 'Ydernummer', 'SghAfd-kode', 'Regionskode', 'Regionsnavn', 'Enhedsnavn', 
             'P_Postnummer', 'P_By', 'Postadresse', 
             'B_Postnummer', 'B_By', 'Besoegsadresse',
             'A_Postnummer', 'A_By', 'Aktivitetsadresse'])
    .collect())

temp_frame.columns = ['SOR_code', 'Ydernummer', 'SHAK_code', 'Region_code', 'Region_name', 'Unit_name', 
             'Postal_postnummer', 'Postal_city', 'Postal_adresse', 
             'Visitation_postnummer', 'Visitation_city', 'Visitation_address',
             'Activity_postnummer', 'Activity_city', 'Activity_address']

temp_frame.write_csv(file = file_final_org, separator=';')

(pl.read_csv(file_final_org, 
            separator=';', 
            schema_overrides={'SghAfd-kode':pl.String, "Telefon":pl.String, "B_Postnummer":pl.String})
    .filter(pl.col('Ydernummer').is_not_null()))

## I move on to the SOR and SHAK codes: 
# first the SHAK
url_shak = "https://sor-filer.sundhedsdata.dk/sor_produktion/data/shak/shakcomplete/shakcomplete.txt"
query_parameters = {"downloadformat": "csv"}
file_url_shak = "/home/jenswaaben/phd/software/adress_mapping/temp_data/shak.csv"
file_url_shak_pd = "/home/jenswaaben/phd/software/adress_mapping/temp_data/shak_pd.csv"
file_final_shak = "/home/jenswaaben/phd/software/adress_mapping/data/shak.csv"

response = requests.get(url_shak, params=query_parameters)
text = response.content.decode("ISO-8859-1")

with open(file_url_shak, mode="w", encoding='utf-8') as file:
    file.write(text)

widths = [3, 20, 8, 8, 8, 120, 3, 3, 3, 3, 3, 1, 2, 2, 1, 25, 1]
names = ['RecArt', 'SHAK_code', 'DatoStart', 'DatoChange', 'DatoEnd', 'Codetext', 
         'Agrp', 'Bgrp', 'Cgrp', 'SKS', 'Egrp', 'Aval', 'Bval', 'Cval', 'Dval', 
         'Inclusion', 'ExtraReg']
names_new = []

pd_df = pd.read_fwf(file_url_shak, widths=widths, header = None)
pd_df.columns = names
pd_df.to_csv(file_url_shak_pd, sep=';', index = False)

# now the SOR codes 
url_SOR = "https://sor-filer.sundhedsdata.dk/sor_produktion/data/sor/sorcsv/V_1_2_1_19/sor.csv"
query_parameters = {"downloadformat": "csv"}
file_url_sor = "/home/jenswaaben/phd/software/adress_mapping/temp_data/sor.csv"
file_url_sor_pd = "/home/jenswaaben/phd/software/adress_mapping/temp_data/sor_pd.csv"
file_final_sor = "/home/jenswaaben/phd/software/adress_mapping/data/sor.csv"

response = requests.get(url_SOR, params=query_parameters)
text = response.content.decode("ISO-8859-1")

with open(file_url_sor, mode="w", encoding='utf-8') as file:
    file.write(text)

sor_data = pl.read_csv(file_url_sor, separator=';')
sor_data.columns
relevant_columns = ['Ydernummer', 
    'Enhedsnavn', 'Enhedstype', 'SghAfd-kode', 
    'Lokationsnummer', 'Region', 
    'SOR-type', 'SOR-kode', 
    'Aktivitetsadresse', 'A_Postnummer', 'A_By', 'A_KK', 'A_Region', 'A_VK', 'A_X', 'A_Y', 
    'Besoegsadresse', 'B_Postnummer', 'B_By','B_KK', 'B_Region', 'B_VK', 'B_X', 'B_Y',
    'Postadresse', 'P_Postnummer', 'P_By','P_KK', 'P_Region', 'P_VK', 'P_X', 'P_Y',
    'Apoteksnummer', 
    'Geografisk_lokalisation']
new_names = ['Ydernummer', 
    'Unit_name', 'Unit_type', 'SHAK_code', 
    'Location_number', 'Region', 
    'SOR_type', 'SOR_code', 
    'Activity_address', 'Activity_postnummer', 'Activity_city', 'Activity_municipality_code', 'Activity_region', 'Activity_road_code', 'Activity_X_coord', 'Activity_Y_coord', 
    'Visitation_address', 'Visitation_postnummer', 'Visitation_city', 'Visitation_municipality_code', 'Visitation_region', 'Visitation_road_code', 'Visitation_X_coord_easting', 'Visitation_Y_coord_northing',
    'Postal_address', 'Postal_postnummer', 'Postal_city','Postal_municipality_code', 'Postal_region', 'Postal_road_code', 'Postal_X_coord', 'Postal_Y_coord',
    'Pharmacy_number', 
    'Geographical_location']


sor_relevant = sor_data.select(relevant_columns)
sor_relevant.columns = new_names

sor_relevant.write_csv(file_final_sor, 
                       separator=';')


## Now for some collected table: 

df_sor = sor_relevant
df_shak = shak_relevant = pl.read_csv(file_url_shak_pd, separator=';')
df_org = pl.read_csv(file_final_org, separator=';', schema_overrides={'SHAK_code':pl.String, 'Visitation_postnummer':pl.String}) 


sor_shaks = df_sor.select(pl.col('SHAK_code')).filter(pl.col('SHAK_code').is_not_null()).sort(by = 'SHAK_code').unique()
shak_shaks = df_shak.select(pl.col('SHAK_code')).filter(pl.col('SHAK_code').is_not_null()).sort(by = 'SHAK_code').unique()
org_shaks = df_org.select(pl.col('SHAK_code')).filter(pl.col('SHAK_code').is_not_null()).sort(by = 'SHAK_code').unique()

sor_shaks_base = sor_shaks.with_columns(base_shak = pl.col('SHAK_code').str.slice(offset = 0, length=4))
shak_shaks_base = shak_shaks.with_columns(base_shak = pl.col('SHAK_code').str.slice(offset = 0, length=4))
org_shaks_base = org_shaks.with_columns(base_shak = pl.col('SHAK_code').str.slice(offset = 0, length=4))

sor_unique_base = sor_shaks_base.select('base_shak').unique().to_series()
shak_unique_base = shak_shaks_base.select('base_shak').unique().to_series()
org_unique_base = org_shaks_base.select('base_shak').unique().to_series()

np.sum(sor_unique_base.is_in(shak_unique_base).to_list()) / sor_unique_base.len()
np.sum(sor_unique_base.is_in(org_unique_base).to_list()) / sor_unique_base.len()
np.sum(org_unique_base.is_in(shak_unique_base).to_list()) / org_unique_base.len()
np.sum(org_unique_base.is_in(sor_unique_base).to_list()) / org_unique_base.len()
np.sum(org_unique_base.is_in(sor_unique_base).to_list()) / org_unique_base.len()
np.sum(sor_unique_base.is_in(org_unique_base).to_list()) / sor_unique_base.len()

####
# This last part is for when i get to using the API as 
####

####
# cleaning the SOR codes and getting the coordinates: 
####

pd_sor = sor_data.to_pandas()
pl_sor = (sor_data
    .with_columns(pl.col('A_X').str.replace_all(',', '.').cast(pl.Float32), 
                  pl.col('A_Y').str.replace_all(',', '.').cast(pl.Float32)))
pl_sor_rel = (sor_relevant
    .with_columns(pl.col('Activity_X_coord').str.replace_all(',', '.').cast(pl.Float32), 
                  pl.col('Activity_Y_coord').str.replace_all(',', '.').cast(pl.Float32)))

# I take the SOR file as it already has coordinates
# First the yder: 
yder_adresse = (pl_sor_rel
    .filter(pl.col('Ydernummer').is_not_null())
    .with_columns(end_coord_x = replace_levels(level_1 = 'Visitation_X_coord_easting', level_2 = 'Activity_X_coord', level_3 = 'Postal_X_coord'), 
                  end_coord_y = replace_levels(level_1 = 'Visitation_Y_coord_northing', level_2 = 'Activity_Y_coord', level_3 = 'Postal_Y_coord'), 
                  end_postnummer = replace_levels(level_1 = 'Visitation_postnummer', level_2 = 'Activity_postnummer', level_3 = 'Postal_postnummer'), 
                  end_region = replace_levels(level_1 = 'Visitation_region', level_2 = 'Activity_region', level_3 = 'Postal_region'))
    .with_columns(pl.col('end_coord_x').str.replace_all(',', '.').cast(pl.Float32), 
                  pl.col('end_coord_y').str.replace_all(',', '.').cast(pl.Float32))
    .select(['SHAK_code', 'Unit_type', 'Unit_name', 'SOR_code', 'Ydernummer', 'end_coord_x', 'end_coord_y', 'end_postnummer', 'end_region'])
    .drop_nulls())

list_coords = [] 
for x,y in zip(yder_adresse['end_coord_x'], yder_adresse['end_coord_y']): 
    list_coords.append(Point(x,y))

yder_gdf = gpd.GeoDataFrame({'Ydernummer': yder_adresse['Ydernummer'], 
                             'geometry':list_coords}, crs="EPSG:25832").to_crs("EPSG:4326")

yder_gdf.to_file('/home/jenswaaben/phd/software/adress_mapping/data/yder.geojson', driver = 'GeoJSON')

# Now for the SHAK in the SOR file: 
shak_replaced = (pl_sor_rel
    .filter(pl.col('SHAK_code').is_not_null())
    .with_columns(end_coord_x = replace_levels(level_1 = 'Visitation_X_coord_easting', level_2 = 'Activity_X_coord', level_3 = 'Postal_X_coord'), 
                  end_coord_y = replace_levels(level_1 = 'Visitation_Y_coord_northing', level_2 = 'Activity_Y_coord', level_3 = 'Postal_Y_coord'), 
                  end_postnummer = replace_levels(level_1 = 'Visitation_postnummer', level_2 = 'Activity_postnummer', level_3 = 'Postal_postnummer'), 
                  end_region = replace_levels(level_1 = 'Visitation_region', level_2 = 'Activity_region', level_3 = 'Postal_region'))
    .with_columns(pl.col('end_coord_x').str.replace_all(',', '.').cast(pl.Float32), 
                  pl.col('end_coord_y').str.replace_all(',', '.').cast(pl.Float32))
    .filter(pl.col('end_coord_x').is_not_null())
    .sort('SHAK_code')
    .select(['SHAK_code', 'Unit_type', 'Unit_name', 'SOR_code', 'Ydernummer', 'end_coord_x', 'end_coord_y', 'end_postnummer', 'end_region']))

list_coords = [] 
for x,y in zip(shak_replaced['end_coord_x'], shak_replaced['end_coord_y']): 
    list_coords.append(Point(x,y))
pd_shak = shak_replaced.to_pandas().drop(columns=['end_coord_x', 'end_coord_y'])

shak_gdf = gpd.GeoDataFrame(pd_shak, geometry = list_coords, crs="EPSG:25832").to_crs("EPSG:4326")

shak_gdf.to_file('/home/jenswaaben/phd/software/adress_mapping/data/shak_from_sor.geojson', driver = 'GeoJSON')

# And lastly the SOR numbers: 
sor_replaced = (pl_sor_rel
    .filter(pl.col('SOR_code').is_not_null())
    .with_columns(end_coord_x = replace_levels(level_1 = 'Visitation_X_coord_easting', level_2 = 'Activity_X_coord', level_3 = 'Postal_X_coord'), 
                  end_coord_y = replace_levels(level_1 = 'Visitation_Y_coord_northing', level_2 = 'Activity_Y_coord', level_3 = 'Postal_Y_coord'), 
                  end_postnummer = replace_levels(level_1 = 'Visitation_postnummer', level_2 = 'Activity_postnummer', level_3 = 'Postal_postnummer'), 
                  end_region = replace_levels(level_1 = 'Visitation_region', level_2 = 'Activity_region', level_3 = 'Postal_region'))
    .with_columns(pl.col('end_coord_x').str.replace_all(',', '.').cast(pl.Float32), 
                  pl.col('end_coord_y').str.replace_all(',', '.').cast(pl.Float32))
    .filter(pl.col('end_coord_x').is_not_null())
    .sort('SOR_code')
    .select(['SOR_code', 'SOR_type','Unit_type', 'Unit_name', 'SHAK_code', 'Ydernummer', 'end_coord_x', 'end_coord_y', 'end_postnummer', 'end_region']))

list_coords = [] 
for x,y in zip(sor_replaced['end_coord_x'], sor_replaced['end_coord_y']): 
    list_coords.append(Point(x,y))

pd_sor = sor_replaced.to_pandas().drop(columns=['end_coord_x', 'end_coord_y'])

sor_gdf = gpd.GeoDataFrame(pd_sor, geometry = list_coords, crs="EPSG:25832").to_crs("EPSG:4326")

sor_gdf.to_file('/home/jenswaaben/phd/software/adress_mapping/data/sor.geojson', driver = 'GeoJSON')

