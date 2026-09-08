library("tidyverse")
library("sf")
library("plotDK")
library("plotly")
library("purrr")
library("paletteer")
options(pillar.sigfig = 10)

# reading population data:
population_data <- read_tsv("data/residence_data_split.tsv") |>
    group_by(postalcode_name, postal_code) |>
    summarise(count = median(count)) |>
    ungroup() |>
    arrange(postal_code)

# Plotting all of Denmark
denmark_g <- sf::st_read("data/denmark.geojson")
denmark_coord <- as_tibble(st_coordinates(denmark_g)) |>
    group_by(L1, L2, L3) |>
    mutate(
        order = row_number(),
        group_id = cur_group_id()
    ) |>
    ungroup()

denmark_min_x <- denmark_coord |>
    pull(X) |>
    min()
denmark_max_x <- denmark_coord |>
    pull(X) |>
    max()
denmark_min_y <- denmark_coord |>
    pull(Y) |>
    min()
denmark_max_y <- denmark_coord |>
    pull(Y) |>
    max()

filter_points <- function(point_df) {
    point_df |>
        filter((X < denmark_max_x & Y < denmark_max_y) &
            (X > denmark_min_x & Y > denmark_min_y))
}

denmark_map <- denmark_coord |>
    ggplot(mapping = aes(x = X, y = Y, group = group_id)) +
    geom_polygon(mapping = aes(fill = group_id)) +
    theme_minimal() +
    theme(
        legend.position = "none",
        panel.background = element_rect(color = NA),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    scale_fill_paletteer_c("ggthemes::Orange-Blue Diverging") +
    scale_y_continuous(expand = 0) +
    scale_x_continuous(expand = 0) +
    coord_fixed()

#ggplotly(denmark_map)
denmark_map

# plotting regions:
regions_g <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/regions.geojson") |>
    st_collection_extract(type = c("POLYGON")) |>
    st_cast("MULTIPOLYGON")
region_names <- regions_g |>
    st_drop_geometry() |>
    as_tibble() |>
    mutate(L3 = row_number()) |>
    select(L3, navn)
regions_coord <- as_tibble(st_coordinates(regions_g)) |>
    left_join(region_names) |>
    group_by(L1, L2, L3) |>
    mutate(
        order = row_number(),
        group_id = cur_group_id()
    ) |>
    ungroup()

ggplot(data = regions_coord) +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = navn)) +
    theme_minimal() +
    theme(
        legend.position = "none",
        panel.background = element_rect(color = NA),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    scale_fill_paletteer_d("MoMAColors::Alkalay2") +
    scale_y_continuous(expand = 0) +
    scale_x_continuous(expand = 0) +
    coord_fixed()


# Plotting municipality:
municipality_g <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/municipality.geojson") |>
    st_collection_extract(type = c("POLYGON")) |>
    st_cast("MULTIPOLYGON")
municipality_names <- municipality_g |>
    st_drop_geometry() |>
    as_tibble() |>
    mutate(L3 = row_number()) |>
    select(L3, navn)
municipality_coord <- as_tibble(st_coordinates(municipality_g)) |>
    left_join(municipality_names) |>
    group_by(L1, L2, L3) |>
    mutate(
        order = row_number(),
        group_id = cur_group_id()
    ) |>
    ungroup()

ggplot(data = municipality_coord) +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = group_id)) +
    theme_minimal() +
    theme(
        legend.position = "none",
        panel.background = element_rect(color = NA),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    scale_fill_paletteer_c("ggthemes::Orange-Blue Diverging") +
    scale_y_continuous(expand = 0) +
    scale_x_continuous(expand = 0) +
    coord_fixed()


# And postal codes:
postal_codes_g_empty <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/postal_codes.geojson")
postal_codes_g_non_empty <- postal_codes_g_empty[!st_is_empty(postal_codes_g_empty), ]
postal_codes_g <- postal_codes_g_non_empty |>
    st_collection_extract(type = c("POLYGON")) |>
    st_cast("MULTIPOLYGON")
postal_code_area <- postal_codes_g |> st_area()
postal_codes_numbers <- postal_codes_g |>
    st_drop_geometry() |>
    as_tibble() |>
    mutate(L3 = row_number()) |>
    select(L3, navn, nr) |>
    mutate(nr = as.numeric(nr)) |>
    mutate(area = postal_code_area)

# now a small check for populations: 
pst_cd_w_coords <- postal_codes_numbers |> 
  distinct(nr, .keep_all = T)
pst_cd_w_pop <- population_data 

anti_join(x = pst_cd_w_coords, y = pst_cd_w_pop, by = c("nr" = "postal_code"))
anti_join(y = pst_cd_w_coords, x = pst_cd_w_pop, by = c("postal_code" = "nr"))

postal_codes_coord <- st_coordinates(postal_codes_g) |>
    as_tibble() |>
    left_join(postal_codes_numbers) |>
    left_join(pst_cd_w_pop, by = c("nr" = "postal_code")) |> 
    replace_na(list("count" = 1)) |> 
    group_by(L1, L2, L3) |>
    mutate(
        order = row_number(),
        group_id = cur_group_id()
    ) |>
    ungroup() |> 
    group_by(group_id) |> 
    mutate(pop_per_sqkm = (count + 1) / (as.numeric(area) / 1000000)) |> 
    drop_na() |> 
    ungroup()

plot_pop <- ggplot(data = postal_codes_coord |> filter(pop_per_sqkm < 2000)) +
  geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = pop_per_sqkm)) + 
  theme_minimal() + 
  theme(
    panel.background = element_rect(color = NA),
    panel.grid.major = element_blank(),
    panel.grid.minor = element_blank(),
    axis.text = element_blank(),
    axis.title = element_blank()
  ) +
  scale_fill_paletteer_c(transform = "log", 
                        breaks = scales::breaks_log(), 
                        labels = scales::label_comma(big.mark = " "), 
                        palette = "scico::cork",
                        na.value = "#29567d") +
  scale_y_continuous(expand = 0) +
  scale_x_continuous(expand = 0) +
  coord_fixed()

plotly_json(plot_pop)

ggplotly(plot_pop)

# And now for plotting the yder codes:
yder_raw <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/yder.geojson")
yder_numbers <- yder_raw |>
    as_tibble() |>
    select(Ydernummer)
yder_coords <- yder_raw |>
    st_coordinates() |>
    as_tibble() |>
    bind_cols(yder_numbers)



p_denmark_yder <- municipality_coord |>
    ggplot() +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id), fill = "#8791eb", color = "white") +
    geom_point(
        data = yder_coords,
        mapping = aes(x = X, y = Y),
        shape = 21,
        alpha = 0.7,
        fill = "orange",
        color = "black",
        size = 2.5,
        stroke = 0.3
    ) +
    theme_minimal() +
    theme(
        legend.position = "none",
        panel.background = element_rect(color = "black", fill = "#f8f5ef"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    coord_fixed()

ggsave(
    filename = "/home/jenswaaben/phd/software/adress_mapping/figures/denmark_yder.png",
    plot = p_denmark_yder,
    dpi = 300
)

# And for the shak codes:
shak_raw <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/shak_from_sor.geojson")
shak_numbers <- shak_raw |>
    as_tibble() |>
    select(-geometry)
shak_coords <- shak_raw |>
    st_coordinates() |>
    as_tibble() |>
    bind_cols(shak_numbers)
shak_coords |>
    filter_points()


plot_shak <- (denmark_coord |>
    ggplot() +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id), fill = "#c7212f") +
    geom_point(
        data = shak_coords,
        mapping = aes(x = X, y = Y, fill = Unit_type),
        shape = 21,
        alpha = 0.7,
        color = "black",
        size = 2.5,
        stroke = 0.3
    ) +
    theme_minimal() +
    theme(
        # legend.position = "none",
        panel.background = element_rect(color = "black", fill = "#f8f5ef"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    guides(fill = guide_legend(ncol = 1)))

ggsave(
    filename = "/home/jenswaaben/phd/software/adress_mapping/figures/denmark_shak.png",
    plot = plot_shak,
    dpi = 300
)


# And lastly for the SOR plots:
sor_raw <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/sor.geojson")
sor_numbers <- sor_raw |>
    as_tibble() |>
    select(-geometry)
sor_coords <- sor_raw |>
    st_coordinates() |>
    as_tibble() |>
    bind_cols(sor_numbers)
sor_coords |>
    filter_points()


plot_sor <- (denmark_coord |>
    ggplot() +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id), fill = "#c7212f") +
    geom_point(
        data = sor_coords,
        mapping = aes(x = X, y = Y, fill = SOR_type),
        shape = 21,
        alpha = 0.7,
        color = "black",
        size = 2.5,
        stroke = 0.3
    ) +
    theme_minimal() +
    theme(
        # legend.position = "none",
        panel.background = element_rect(color = "black", fill = "#f8f5ef"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    guides(fill = guide_legend(ncol = 1)))

ggsave(
    filename = "/home/jenswaaben/phd/software/adress_mapping/figures/denmark_sor.png",
    plot = plot_sor,
    dpi = 300
)

# the pharmacies: 
pharmacy_data <- read_tsv("data/list_pharmacies.tsv") 

pharm_plot <- ggplot(data = postal_codes_coord |> mutate(pop_per_sqkm  = scales::squish(pop_per_sqkm,  c(0, 20000)))) +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = pop_per_sqkm), color = "grey50", linewidth = 0.2) +
    scale_fill_gradientn(transform = "log", 
                         breaks = scales::breaks_log(), 
                         labels = scales::label_comma(big.mark = " ", accuracy = 0.1), 
                         colors = paletteer::paletteer_c("ggthemes::Orange-Blue-White Diverging", n = 3, direction = -1),
                         na.value = "#29567d", 
                         name = "Population per km^2 (20 000 max)") + 
    geom_point(data = pharmacy_data, 
               mapping = aes(x = longitude, y = lattitude), 
               shape = 21, 
               size = 2, 
               fill = "#f79cd4") + 
    theme_minimal() +
    theme(
      panel.background = element_rect(color = "black", fill = "#f8f5ef"),
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      axis.text = element_blank(),
      axis.title = element_blank()
    ) + 
    coord_fixed() + 
    scale_x_continuous(expand = 0) + 
    scale_y_continuous(expand = 0) 

plotly_obj <- ggplotly(pharm_plot)

id_filter <- postal_codes_coord |> distinct(group_id, postalcode_name)
named_list <- id_filter |> pull(postalcode_name)
names(named_list) <- id_filter |> pull(group_id)
for (postcode in 1:(length(plotly_obj$x$data) - 2)){
  gid <- str_extract(plotly_obj$x$data[[postcode]]$text, "[:digit:]+") 
  plotly_obj$x$data[[postcode]]$text <- named_list[as.character(gid)]
}


plotly_obj$x$data[[length(plotly_obj$x$data) - 1 ]]$text <- str_c(pharmacy_data$pharmacy_name, "\n", pharmacy_data$city)
plotly_obj
