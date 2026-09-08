library("tidyverse")
library("sf")
library("plotDK")
library("plotly")
library("purrr")
library("paletteer")

residence_data_split <- read_tsv("data/dst_residence_numbers.tsv") |>
    mutate(
        municipality_code = str_extract(
            string = municipality,
            pattern = "[:digit:]+"
        ),
        postal_code = str_extract(
            string = postcode,
            pattern = "[:digit:]+"
        ),
        municipality = str_remove(municipality, "^[:digit:]+ "),
        postalcode_name = str_remove(postcode, "^[:digit:]+ ")
    ) |>
    filter(municipality != "Hele landet") |>
    select(municipality, municipality_code, postalcode_name, postal_code, year, count)



write_tsv(
    x = residence_data_split,
    "data/residence_data_split.tsv"
)
