import os
import numpy as np
import requests
import pandas as pd
import polars as pl

# list of all the tables in the data: 
base = "https://api.statbank.dk/v1/tables" 
files = requests.post(base)
data = files.json()
[[x["id"], x["text"]] for x in data]

# tableinfo for the one I want: 
base = "https://api.statbank.dk/v1/tableinfo" 
payload = {"table": "POSTNR2", 
           "format" : "JSONSTAT"}

files = requests.post(base,  json=payload)
data = files.json()
data["variables"]

# Now for extracting the actual data: 
base = "https://api.statbank.dk/v1/data" 
payload = {"table": "POSTNR2", 
           "format" : "JSONSTAT", 
           "variables": [
               {"code":"PNR20", 
                "values": ["*"]}, 
               {"code":"Tid", 
                "values":["*"]}
           ]}

files = requests.post(base,  json=payload)
data = files.json()
data["dataset"]["dimension"]
len(data["dataset"]["value"])
total_rows = len(data["dataset"]["dimension"]["PNR20"]["category"]["label"].values())
total_cols = len(data["dataset"]["dimension"]["Tid"]["category"]["label"].values())
name_series = pl.Series(data["dataset"]["dimension"]["PNR20"]["category"]["label"].values())

(pl.from_pandas(pd.DataFrame(np.matrix(data=data["dataset"]["value"]).reshape(total_rows, total_cols)))
 .with_columns(name_series.alias("place"))
 .with_columns(pl.col("place").str.split(" - ")) 
 .with_columns(pl.col("place").list[0].alias("municipality"), 
               pl.col("place").list[-1].alias("postcode")))



# Now for extracting the actual data: 
base = "https://api.statbank.dk/v1/data" 
payload = {"table": "POSTNR2", 
           "format" : "CSV", 
           "variables": [
               {"code":"PNR20", 
                "values": ["*"]}, 
               {"code":"Tid", 
                "values":["*"]}
           ]}

files = requests.post(base,  json=payload)
data = files.text
list_data = [list.split(";") for list in data.split("\r\n")]
series_data = (pl.DataFrame(pl.Series(list_data)[1:-1].alias("combined_data"))
               .with_columns(pl.col("combined_data").list[0].alias("place"), 
                             pl.col("combined_data").list[1].alias("year"), 
                             pl.col("combined_data").list[2].alias("count"))
             .with_columns(pl.col("place").str.split(" - ")) 
             .with_columns(pl.col("place").list[0].alias("municipality"), 
                           pl.col("place").list[-1].alias("postcode"))
             .select(pl.col(["municipality", "postcode", "year", "count"])))

series_data.write_csv("data/dst_residence_numbers.tsv", separator="\t")