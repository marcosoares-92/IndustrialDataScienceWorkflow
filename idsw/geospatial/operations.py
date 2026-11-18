"""
idsw.geospatial.operations
==========================
Geospatial geometric operations covering spatial joins, buffer creation,
spatial overlays, geometry dissolving, and feature attribute calculations.
"""

import numpy as np
import pandas as pd

from idsw import InvalidInputsError, ControlVars


def spatial_join(left_gdf, right_gdf, how = 'inner', predicate = 'intersects'):
    """
    spatial_join:
    Performs a spatial join between two GeoDataFrames based on geometric predicates
    ('intersects', 'contains', 'within', 'touches', 'crosses').

    : param: left_gdf: geopandas.GeoDataFrame.
    : param: right_gdf: geopandas.GeoDataFrame.
    : param: how: 'inner', 'left', or 'right'.
    : param: predicate: spatial relationship predicate (default 'intersects').
    : return: geopandas.GeoDataFrame with joined attributes.
    """
    try:
        import geopandas as gpd

        # Ensure matching CRS
        if left_gdf.crs != right_gdf.crs:
            right_gdf = right_gdf.to_crs(left_gdf.crs)

        joined_gdf = gpd.sjoin(left_gdf, right_gdf, how = how, predicate = predicate)

        if ControlVars.show_results:
            print(f"Spatial join completed ({how} join with predicate '{predicate}'): {len(joined_gdf)} resulting rows.")

        return joined_gdf

    except ImportError:
        raise InvalidInputsError("Geopandas is required for spatial joins. Run: pip install geopandas")


def create_spatial_buffers(gdf, distance = 100.0, resolution = 16):
    """
    create_spatial_buffers:
    Constructs geographic buffer zones around spatial geometries.

    : param: gdf: geopandas.GeoDataFrame.
    : param: distance: buffer radius in CRS coordinate units (meters if UTM / projected).
    : param: resolution: number of segments used to approximate a quarter circle.
    : return: geopandas.GeoDataFrame with buffered geometry column.
    """
    try:
        import geopandas as gpd

        buffered_gdf = gdf.copy()
        buffered_gdf['geometry'] = gdf.geometry.buffer(distance = distance, resolution = resolution)

        if ControlVars.show_results:
            print(f"Constructed spatial buffers with radius {distance} units.")

        return buffered_gdf

    except ImportError:
        raise InvalidInputsError("Geopandas is required for spatial buffers.")


def dissolve_geometries(gdf, by = None, aggfunc = 'first'):
    """
    dissolve_geometries:
    Dissolves and merges neighboring or related geometries sharing an attribute into multipart geometries.

    : param: gdf: geopandas.GeoDataFrame.
    : param: by: column name to group by. If None, dissolves all geometries into a single union geometry.
    : param: aggfunc: aggregation function for non-spatial columns ('first', 'mean', 'sum').
    : return: dissolved geopandas.GeoDataFrame.
    """
    try:
        import geopandas as gpd

        dissolved_gdf = gdf.dissolve(by = by, aggfunc = aggfunc).reset_index()

        if ControlVars.show_results:
            print(f"Geometries dissolved by '{by}': reduced from {len(gdf)} to {len(dissolved_gdf)} rows.")

        return dissolved_gdf

    except ImportError:
        raise InvalidInputsError("Geopandas is required.")


def calculate_spatial_features(gdf):
    """
    calculate_spatial_features:
    Calculates geographic metrics for each geometry:
    area, length/perimeter, centroid coordinates (lat, lon), and bounding box extents.

    : param: gdf: geopandas.GeoDataFrame.
    : return: GeoDataFrame augmented with spatial metric columns.
    """
    try:
        res_gdf = gdf.copy()
        res_gdf['spatial_area'] = res_gdf.geometry.area
        res_gdf['spatial_length'] = res_gdf.geometry.length

        centroids = res_gdf.geometry.centroid
        res_gdf['centroid_x'] = centroids.x
        res_gdf['centroid_y'] = centroids.y

        bounds = res_gdf.geometry.bounds
        res_gdf['min_x'] = bounds['minx']
        res_gdf['min_y'] = bounds['miny']
        res_gdf['max_x'] = bounds['maxx']
        res_gdf['max_y'] = bounds['maxy']

        return res_gdf

    except Exception as e:
        print(f"Spatial features calculation note: {e}")
        return gdf
