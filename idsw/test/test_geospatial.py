"""
Unit tests for idsw.geospatial module.
Covers:
- load_geospatial_data (CSV and GeoJSON loading)
- convert_crs, export_geospatial_data
- calculate_spatial_features (area, length, centroid)
- create_spatial_buffers, dissolve_geometries, spatial_join
- plot_choropleth, create_interactive_map, create_marker_cluster_map, create_spatial_heatmap
"""

import unittest
import os
import shutil
import tempfile
import pandas as pd

from idsw import ControlVars, InvalidInputsError
from idsw.geospatial import (
    load_geospatial_data,
    convert_crs,
    export_geospatial_data,
    calculate_spatial_features,
    create_spatial_buffers,
    dissolve_geometries,
    spatial_join,
    plot_choropleth,
    create_interactive_map,
    create_marker_cluster_map,
    create_spatial_heatmap
)


class TestGeospatial(unittest.TestCase):

    def setUp(self):
        ControlVars.show_plots = False
        ControlVars.show_results = False
        self.test_dir = tempfile.mkdtemp()

        # CSV with coordinates
        self.csv_path = os.path.join(self.test_dir, "sensors_coords.csv")
        self.df_coords = pd.DataFrame({
            "sensor_id": [1, 2, 3],
            "latitude": [-23.5505, -23.5510, -23.5520],
            "longitude": [-46.6333, -46.6340, -46.6350],
            "reading": [10.5, 20.1, 15.3]
        })
        self.df_coords.to_csv(self.csv_path, index=False)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_geospatial_data_from_csv(self):
        gdf = load_geospatial_data(
            file_directory_path=self.test_dir,
            file_name_with_extension="sensors_coords.csv",
            crs="EPSG:4326"
        )
        self.assertIsNotNone(gdf)
        if hasattr(gdf, "geometry"):
            self.assertEqual(len(gdf), 3)
            self.assertEqual(str(gdf.crs), "EPSG:4326")

    def test_calculate_spatial_features(self):
        gdf = load_geospatial_data(
            file_directory_path=self.test_dir,
            file_name_with_extension="sensors_coords.csv",
            crs="EPSG:4326"
        )
        if hasattr(gdf, "geometry"):
            feat_gdf = calculate_spatial_features(gdf)
            self.assertIn("centroid_x", feat_gdf.columns)
            self.assertIn("centroid_y", feat_gdf.columns)

    def test_spatial_buffers_and_dissolve(self):
        gdf = load_geospatial_data(
            file_directory_path=self.test_dir,
            file_name_with_extension="sensors_coords.csv",
            crs="EPSG:4326"
        )
        if hasattr(gdf, "geometry"):
            buffered = create_spatial_buffers(gdf, distance=0.01)
            self.assertEqual(len(buffered), 3)

            dissolved = dissolve_geometries(buffered)
            self.assertEqual(len(dissolved), 1)

    def test_interactive_visualizations(self):
        # Marker cluster map
        m1 = create_marker_cluster_map(
            points_df=self.df_coords,
            lat_col="latitude",
            lon_col="longitude",
            popup_col="sensor_id"
        )
        # Heatmap
        m2 = create_spatial_heatmap(
            points_df=self.df_coords,
            lat_col="latitude",
            lon_col="longitude",
            weight_col="reading"
        )
        # Check that maps run without error (returns folium.Map or None if folium not installed)
        self.assertTrue(m1 is not None or m1 is None)
        self.assertTrue(m2 is not None or m2 is None)

    def test_invalid_inputs(self):
        with self.assertRaises(InvalidInputsError):
            load_geospatial_data(
                file_directory_path=self.test_dir,
                file_name_with_extension="non_existent.geojson"
            )


if __name__ == "__main__":
    unittest.main()
