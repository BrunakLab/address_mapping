import requests
import openpyxl
import pandas as pd
import polars as pl

# loading API created through datafordeleren
with open("api.txt", "r") as f:
    lines = f.readlines()

# My API key and the base URL for the API 
API_KEY = lines[0].strip()
URL = "https://api.datafordeler.dk/dar/graphql"

# client and list for the API: 
#URL = "https://graphql.datafordeler.dk/DAR/v3?"

# loading excel
active_pharmacies = pl.read_csv(source="data/list_pharmacies.tsv", separator="\t")
inactive_pharmacies = (pl.read_excel("data/old_pharmacies.xlsx", sheet_name="Inaktive Apoteksenheder")
                       .select(pl.col(["postcode", "city", "grant_holder", "pharmacy_number", "filial_number"]))
                       .with_columns(pl.col("pharmacy_number").cast(dtype=pl.String).str.slice(length=3, offset = 0).str.pad_start(fill_char="0", length=3), 
                                     pl.col("filial_number").fill_null(9).cast(dtype = pl.String).str.pad_start(fill_char="0", length = 2)) 
                       .with_columns(pl.concat_str(pl.col("pharmacy_number"),pl.col("filial_number")).alias("ibnr"))
                       .with_columns(pl.col("grant_holder").str.extract(r', ([^,]+),').alias("pharmacy_name"), 
                                     pl.lit("").alias("address"), 
                                     pl.lit("inactive").alias("pharmacy_types"), 
                                     pl.lit("unfilled").alias("search_string"), 
                                     pl.lit(0).cast(dtype = pl.Float64).alias("lattitude"), 
                                     pl.lit(0).cast(dtype = pl.Float64).alias("longitude"), 
                                     pl.lit("unfilled").alias("found_address"))
                       .select(pl.col("pharmacy_number", "filial_number", "pharmacy_name", "address", "postcode", 
                                      "city", "pharmacy_types", "ibnr", "search_string", "lattitude", "longitude", "found_address"))
                       .unique(keep="first", subset=["ibnr"]))

# saving it: 
inactive_pharmacies.write_csv(file="data/list_pharmacies_inactive_pre.tsv", separator= "\t")

# This file is added to mistral to give coordinates
data = pl.read_csv(source="data/list_pharmacies_inactive_pre.tsv", separator="\t")