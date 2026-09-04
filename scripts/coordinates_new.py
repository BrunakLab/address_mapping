import os
import requests
import pandas as pd
import polars as pl

# generate your own API on https://danskadresseapi.dk/
API_key = "your_api"

data = (pl.read_excel(source = "data/list_pharmacies.xlsx")
        .rename(mapping={"Apoteksnummer (apoteksenhed)":"pharmacy_number", 
                         "Filialnummer (apoteksenhed)": "filial_number", 
                         "Virksomhedsnavn": "pharmacy_name", 
                         "Adresselinje 1": "address", 
                         "Postnummer": "postcode", 
                         "By": "city", 
                         "Enhedsrolle Navn":"pharmacy_types"})
        .with_columns(pl.col("filial_number").fill_null(0).cast(pl.String).str.pad_start(2, "0"))
        .with_columns((pl.col("pharmacy_number").cast(pl.String).str.pad_start(3, "0") + pl.col("filial_number")).alias("ibnr"))
        .with_columns((pl.col("address") + pl.lit(", ") + pl.col("postcode")).alias("search_string")))


# now for getting the coordinates: 
sub_sample = 541
address_series = data["search_string"].to_list()[0:sub_sample]
city_series = data["city"].to_list()
postcode_series = data["postcode"].to_list()

for i, address in enumerate(address_series): 
    if i == 0: 
        lattitude_list = []
        longitude_list = []
        found_address_list = []
    r = requests.get(
        'https://api.danskadresseapi.dk/dawa/autocomplete',
        params={'q': address},
        headers={'Authorization': f'Bearer api'})
    results = r.json()
    if results == []: 
        r = requests.get(
                'https://api.danskadresseapi.dk/dawa/autocomplete',
                params={'q': postcode_series[i]},
                headers={'Authorization': f'Bearer api'})
        results = r.json()
        if results == []: 
            lattitude = pl.Null
            longitude = pl.Null
        else: 
            lattitude = results[0]["data"]["y"]
            longitude = results[0]["data"]["x"]
        lattitude_list.append(lattitude)
        longitude_list.append(longitude)
        found_address_list.append("first postcode address")
    else: 
        lattitude = results[0]["data"]["y"]
        longitude = results[0]["data"]["x"]
        lattitude_list.append(lattitude)
        longitude_list.append(longitude)
        found_address_list.append("road")



pharmacy_data = (data[0:sub_sample]
 .with_columns(pl.Series(lattitude_list).alias("lattitude"), 
               pl.Series(longitude_list).alias("longitude"), 
               pl.Series(found_address_list).alias("found_address"))
 )

pharmacy_data.write_csv(file = "data/list_pharmacies.csv", 
                        separator=";")