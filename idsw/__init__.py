__doc__ = """
Industrial Data Science Workflow: full workflow for ETL, statistics, 
and Machine learning modelling of (usually) time-stamped industrial facilities data.
Not only applicable to monitoring quality and industrial facilities systems, the package
can be applied to data manipulation, characterization and modelling of different numeric
and categorical datasets to boost your work and replace tradicional tools like SAS, Minitab
and Statistica software.

Check the project Github: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow
"""

__author__ = """Marco Cesar Prado Soares; Gabriel Fernandes Luz"""
__version__ = "1.2.5"

from .datafetch import *
from .etl import *
from .modelling import *
