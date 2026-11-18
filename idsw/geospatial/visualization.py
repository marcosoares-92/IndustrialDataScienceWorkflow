"""
idsw.geospatial.visualization
=============================
Cartographic and geospatial visualization functions:
- Static choropleth mapping with Matplotlib & GeoPandas
- Interactive Folium web maps with layer controls
- Point and marker cluster maps for dense sensor networks
- Geospatial density heatmaps
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from idsw import InvalidInputsError, ControlVars


def plot_choropleth(
    gdf,
    column,
    cmap = 'viridis',
    legend = True,
    figsize = (10, 8),
    title = None,
    export_png = False,
    file_name = None,
    directory_to_save = None
):
    """
    plot_choropleth:
    Generates a publication-ready thematic choropleth map.

    : param: gdf: geopandas.GeoDataFrame with polygon geometries.
    : param: column: str, column name to visualize thematic values.
    : param: cmap: colormap name (e.g. 'viridis', 'plasma', 'Blues', 'RdYlGn').
    : param: legend: bool, whether to display color bar / legend.
    : param: figsize: tuple (width, height).
    : param: title: str, map title.
    : return: matplotlib Figure and Axes.
    """
    if ControlVars.show_plots:
        fig, ax = plt.subplots(figsize = figsize)
        gdf.plot(
            column = column,
            cmap = cmap,
            legend = legend,
            ax = ax,
            edgecolor = 'black',
            linewidth = 0.5
        )
        ax.set_title(title if title is not None else f"Choropleth Map: {column}")
        ax.axis('off')

        if export_png:
            import os
            d = directory_to_save or ""
            fn = file_name or f"choropleth_{column}"
            out_p = os.path.join(d, fn + ".png")
            plt.savefig(out_p, dpi = 300, bbox_inches = 'tight')
            if ControlVars.show_results:
                print(f"Choropleth map saved to '{out_p}'.")

        plt.show()
        return fig, ax

    return None, None


def create_interactive_map(
    gdf,
    tooltip_columns = None,
    color_column = None,
    tiles = 'CartoDB positron',
    zoom_start = 11
):
    """
    create_interactive_map:
    Renders an interactive Folium leaflet map from a GeoDataFrame.

    : param: gdf: geopandas.GeoDataFrame.
    : param: tooltip_columns: list of attribute columns to display on hover.
    : param: color_column: column name to drive color coding.
    : param: tiles: base map style ('CartoDB positron', 'OpenStreetMap', 'CartoDB dark_matter').
    : return: folium.Map instance.
    """
    try:
        import folium

        # Calculate map center from centroid
        centroid = gdf.to_crs('EPSG:4326').geometry.unary_union.centroid
        m = folium.Map(location = [centroid.y, centroid.x], zoom_start = zoom_start, tiles = tiles)

        # Add GeoJSON layer
        tooltip = folium.GeoJsonTooltip(fields = tooltip_columns) if tooltip_columns else None
        folium.GeoJson(
            gdf.to_crs('EPSG:4326'),
            tooltip = tooltip,
            style_function = lambda x: {
                'fillColor': 'royalblue',
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.5
            }
        ).add_to(m)

        return m

    except ImportError:
        print("[!] Note: 'folium' is required for interactive maps. Run: pip install folium")
        return None


def create_marker_cluster_map(
    points_df,
    lat_col = 'latitude',
    lon_col = 'longitude',
    popup_col = None,
    zoom_start = 10
):
    """
    create_marker_cluster_map:
    Renders an interactive clustered marker map for high-density spatial points (e.g. sensor networks, customer locations).

    : param: points_df: pandas DataFrame or GeoDataFrame.
    : param: lat_col: name of latitude column.
    : param: lon_col: name of longitude column.
    : param: popup_col: column value to show in popup when a marker is clicked.
    : return: folium.Map instance.
    """
    try:
        import folium
        from folium.plugins import MarkerCluster

        lat_mean = float(points_df[lat_col].mean())
        lon_mean = float(points_df[lon_col].mean())

        m = folium.Map(location = [lat_mean, lon_mean], zoom_start = zoom_start, tiles = 'OpenStreetMap')
        marker_cluster = MarkerCluster().add_to(m)

        for _, row in points_df.iterrows():
            lat = row[lat_col]
            lon = row[lon_col]
            popup_txt = str(row[popup_col]) if popup_col and popup_col in row else None
            folium.Marker(location = [lat, lon], popup = popup_txt).add_to(marker_cluster)

        return m

    except ImportError:
        print("[!] Note: 'folium' is required. Run: pip install folium")
        return None


def create_spatial_heatmap(
    points_df,
    lat_col = 'latitude',
    lon_col = 'longitude',
    weight_col = None,
    zoom_start = 10
):
    """
    create_spatial_heatmap:
    Creates a geographic density heatmap using Folium HeatMap plugin.

    : param: points_df: pandas DataFrame with coordinates.
    : param: lat_col: latitude column name.
    : param: lon_col: longitude column name.
    : param: weight_col: optional column weighting point intensity (e.g. sensor readings, sales amount).
    : return: folium.Map instance.
    """
    try:
        import folium
        from folium.plugins import HeatMap

        lat_mean = float(points_df[lat_col].mean())
        lon_mean = float(points_df[lon_col].mean())

        m = folium.Map(location = [lat_mean, lon_mean], zoom_start = zoom_start, tiles = 'CartoDB dark_matter')

        if weight_col and weight_col in points_df.columns:
            heat_data = [[row[lat_col], row[lon_col], float(row[weight_col])] for _, row in points_df.iterrows()]
        else:
            heat_data = [[row[lat_col], row[lon_col]] for _, row in points_df.iterrows()]

        HeatMap(heat_data, radius = 15).add_to(m)
        return m

    except ImportError:
        print("[!] Note: 'folium' is required. Run: pip install folium")
        return None
