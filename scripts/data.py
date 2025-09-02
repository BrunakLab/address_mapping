import polars as pl
from urllib.request import urlretrieve
import requests

# I start with organisations 
# https://statistik.medcom.dk/exports/organisations.zip
url_org = 'https://statistik.medcom.dk/exports/organisations.csv'
query_parameters = {"downloadformat": "csv"}
file_url_org = "/home/jenswaaben/phd/software/adress_mapping/temp_data/org.csv"
file_final_org = "/home/jenswaaben/phd/software/adress_mapping/data/org.csv"

response = requests.get(url_org, params=query_parameters)
text = response.content.decode("ISO-8859-1")

with open(file_url_org, mode="w", encoding='utf-8') as file:
    file.write(text)

(pl.scan_csv(file_url_org, 
            separator=';', 
            schema_overrides={'SghAfd-kode':pl.String, "Telefon":pl.String, "B_Postnummer":pl.String}, 
            truncate_ragged_lines=True)
    .select(['SOR-kode', 'Ydernummer','Regionskode', 'Regionsnavn', 'Enhedsnavn', 
             'P_Postnummer', 'P_By', 'Postadresse', 'B_Postnummer', 'B_By',
             'Besoegsadresse', 'A_Postnummer', 'A_By'])
    .collect()
    .write_csv(file = file_final_org, separator=';'))

(pl.read_csv(file_final_org, 
            separator=';', 
            schema_overrides={'SghAfd-kode':pl.String, "Telefon":pl.String, "B_Postnummer":pl.String})
    .filter(pl.col('Ydernummer').is_not_null()))

# I move on to the SOR and SHAK codes: 
