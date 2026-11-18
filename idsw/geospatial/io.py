"""
idsw.geospatial.io
==================
Functions for importing, exporting, and converting geospatial data files
(GeoJSON, Shapefile, GeoPackage, KML, and CSV with coordinate columns).
Mimics the API style of idsw.datafetch.pipes.load_pandas_dataframe.
"""

import os
import pandas as pd

from idsw import InvalidInputsError, ControlVars


def load_geospatial_data(
    file_directory_path,
    file_name_with_extension,
    crs = None,
    lat_col = None,
    lon_col = None
):
    """
    load_geospatial_data:
    Loads geospatial data files into a GeoPandas GeoDataFrame.
    Supports GeoJSON (.geojson, .json), ESRI Shapefile (.shp), GeoPackage (.gpkg),
    and CSV files containing latitude and longitude coordinates.

    : param: file_directory_path: str, directory containing the file.
    : param: file_name_with_extension: str, file name.
    : param: crs: target coordinate reference system (e.g. 'EPSG:4326', 'EPSG:3857').
    : param: lat_col: str, column name with latitudes if loading a CSV.
    : param: lon_col: str, column name with longitudes if loading a CSV.
    : return: geopandas.GeoDataFrame.
    """
    full_path = os.path.join(file_directory_path, file_name_with_extension)
    if not os.path.exists(full_path):
        raise InvalidInputsError(f"Geospatial file '{full_path}' does not exist.")

    ext = os.path.splitext(file_name_with_extension)[1].lower()

    try:
        import geopandas as gpd
        from shapely.geometry import Point

        if ext in ['.geojson', '.json', '.shp', '.gpkg']:
            gdf = gpd.read_file(full_path)
            if crs is not None and gdf.crs is not None:
                gdf = gdf.to_crs(crs)
            elif crs is not None and gdf.crs is None:
                gdf = gdf.set_crs(crs)

        elif ext in ['.csv', '.txt']:
            df = pd.read_csv(full_path)
            # Detect coordinate columns if not provided
            if lat_col is None or lon_col is None:
                candidates_lat = [c for c in df.columns if c.lower() in ['lat', 'latitude', 'y']]
                candidates_lon = [c for c in df.columns if c.lower() in ['lon', 'long', 'longitude', 'x']]
                if candidates_lat and candidates_lon:
                    lat_col = candidates_lat[0]
                    lon_col = candidates_lon[0]
                else:
                    raise InvalidInputsError("Could not automatically identify latitude/longitude columns in CSV. Specify lat_col and lon_col.")

            geometry = [Point(xy) for xy in zip(df[lon_col], df[lat_col])]
            gdf = gpd.GeoDataFrame(df, geometry = geometry, crs = crs or 'EPSG:4326')

        else:
            gdf = gpd.read_file(full_path)

        if ControlVars.show_results:
            print("=" * 80)
            print(f"GEOSPATIAL DATASET LOADED: '{file_name_with_extension}'")
            print("=" * 80)
            print(f"Total Features/Geometries: {len(gdf)}")
            print(f"CRS (Coordinate Reference System): {gdf.crs}")
            print(f"Geometry Types: {dict(gdf.geometry.geom_type.value_counts())}")
            try:
                from IPython.display import display
                display(gdf.head(5))
            except Exception:
                print(gdf.head(5).to_string())

        return gdf

    except ImportError:
        print("[!] Note: 'geopandas' and 'shapely' are required for geospatial processing. Run: pip install geopandas shapely")
        # Fallback to standard pandas dataframe
        return pd.read_csv(full_path) if ext in ['.csv', '.txt'] else full_path


def convert_crs(gdf, target_crs = 'EPSG:4326'):
    """
    convert_crs:
    Reprojects a GeoDataFrame from its current CRS to a target CRS.
    """
    try:
        import geopandas as gpd
        if isinstance(gdf, gpd.GeoDataFrame):
            return gdf.to_crs(target_crs)
        return gdf
    except Exception as e:
        print(f"CRS conversion note: {e}")
        return gdf


def export_geospatial_data(gdf, file_path, driver = None):
    """
    export_geospatial_data:
    Exports a GeoDataFrame to GeoJSON, Shapefile, or GeoPackage.
    """
    try:
        import geopandas as gpd
        if isinstance(gdf, gpd.GeoDataFrame):
            gdf.to_file(file_path, driver = driver)
            if ControlVars.show_results:
                print(f"Geospatial data successfully exported to '{file_path}'.")
    except Exception as e:
        print(f"Export error: {e}")
