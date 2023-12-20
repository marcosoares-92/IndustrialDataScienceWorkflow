__doc__ = """
idsw.datafetch
===============
Data pipelines for fetching and exporting data to different sources: AWS S3, GCP BigQuery,
AspenTech IP21, MS SQLServer, SQLite files. Also includes functionalities for obtaining 
Pandas dataframes from CSV, Excel or JSON files and saving and importing ML models and other 
objects like lists and dictionaries.
"""

from .core import *
from .pipes import *
