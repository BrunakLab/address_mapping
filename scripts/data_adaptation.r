library("tidyverse")
library("sf")
library("plotly")
library("purrr")
library("paletteer")
library("dplyr")

residence_data_split <- read_tsv("data/dst_residence_numbers.tsv") |>
  mutate(municipality_code = str_extract(string = municipality,
                                         pattern = "[:digit:]+"),
         postal_code = str_extract(string = postcode,
                                   pattern = "[:digit:]+"),
         municipality = str_remove(municipality, "^[:digit:]+ "),
         postalcode_name = str_remove(postcode, "^[:digit:]+ ")) |>
  filter(municipality != "Hele landet") |>
  select(municipality, municipality_code,
         postalcode_name, postal_code, year, count)

write_tsv(x = residence_data_split,
          file = "data/residence_data_split.tsv")

###
# loading the postcode geojson and finding the centers. 
###

# Read postal codes GeoJSON
postal_codes_sf <- st_read("data/postal_codes.geojson", quiet = TRUE)

# Find geometrical centers of each postal code area
postal_centers <- postal_codes_sf |>
    st_centroid() 

postal_centers_for_join <- postal_centers |>
    select(nr, navn) |> 
    st_drop_geometry() |> 
    as_tibble()

postal_centers_tibble <- postal_centers |>
    st_coordinates() |>
    as_tibble() |>
    rename(longitude = X, latitude = Y) |> 
    bind_cols(postal_centers_for_join)

# Join centers back with postal code data
write_tsv(postal_centers_tibble, file = "data/postal_code_centers.tsv")


### 
# 
###
active_pharmacies <- read_tsv("data/list_pharmacies.tsv") |>
    mutate(pharmacy_number = as.character(pharmacy_number), 
           postcode = as.character(postcode)) |> 
    mutate(status = "active") |> 
    rename(c("latitude" = "lattitude"))
inactive_pharmacies <- read_tsv("data/list_pharmacies_inactive_pre.tsv") |> 
    select(-c(longitude, lattitude, city)) |>
    mutate(postcode = as.character(postcode)) |>
    mutate(address = "postalcode_centre") |> 
    left_join(postal_centers_tibble |> distinct(nr, .keep_all = TRUE), by = c("postcode" = "nr")) |>
    mutate(found_address = "centre") |>
    mutate(pharmacy_number = as.character(pharmacy_number)) |> 
    mutate(status = "inactive")

joined_pharmacies <- bind_rows(active_pharmacies, inactive_pharmacies)
write_tsv(x = joined_pharmacies, 
          file = "data/joined_pharmacy_positions.tsv")

ggplot(data = joined_pharmacies) + 
    geom_point(mapping = aes(x = longitude, y = latitude, shape = status))