library("tidyverse")
library("sf")
library("plotDK")
library("plotly")
library("purrr")
library("paletteer")
options(pillar.sigfig = 10)

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

denmark_coord |>
    ggplot(mapping = aes(x = X, y = Y, group = group_id)) +
    geom_polygon(mapping = aes(fill = group_id)) +
    theme_minimal() +
    theme(
        legend.position = "none",
        panel.background = element_rect(color = "black"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        axis.text = element_blank(),
        axis.title = element_blank()
    ) +
    scale_fill_paletteer_c("ggthemes::Orange-Blue Diverging")

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
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = navn))

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
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = navn))

# And postal codes:
postal_codes_g_empty <- sf::st_read("/home/jenswaaben/phd/software/adress_mapping/data/postal_codes.geojson")
postal_codes_g_non_empty <- postal_codes_g_empty[!st_is_empty(postal_codes_g_empty), ]
postal_codes_g <- postal_codes_g_non_empty |>
    st_collection_extract(type = c("POLYGON")) |>
    st_cast("MULTIPOLYGON")
postal_codes_numbers <- postal_codes_g |>
    st_drop_geometry() |>
    as_tibble() |>
    mutate(L3 = row_number()) |>
    select(L3, nr) |>
    mutate(nr = as.numeric(nr))
postal_codes_coord <- st_coordinates(postal_codes_g) |>
    as_tibble() |>
    left_join(postal_codes_numbers) |>
    group_by(L1, L2, L3) |>
    mutate(
        order = row_number(),
        group_id = cur_group_id()
    ) |>
    ungroup()

ggplot(data = postal_codes_coord) +
    geom_polygon(mapping = aes(x = X, y = Y, group = group_id, fill = nr))


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
    )

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
