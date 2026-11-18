"""
idsw.geospatial
===============
Geospatial Data Processing, Spatial Analysis, and Cartographic Visualization for IDSW.
Includes:
- Reading and Exporting GeoJSON, Shapefiles, and Coordinate Files (io.py)
- Spatial Joins, Buffer Zones, and Dissolve Aggregations (operations.py)
- Choropleth Maps, Folium Interactive Maps, Marker Clusters, and Heatmaps (visualization.py)
"""

from .io import *
from .operations import *
from .visualization import *
