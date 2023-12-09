# Industrial Data Science Workflow
## Industrial Data Science Workflow: full workflow for ETL, statistics, and Machine learning modelling of (usually) time-stamped industrial facilities data.
### Not only applicable to monitoring quality and industrial facilities systems, the package can be applied to data manipulation, characterization and modelling of different numeric and categorical datasets to boost your work and replace tradicional tools like SAS, Minitab and Statistica software.

Check the project Github: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow

Authors:
- Marco Cesar Prado Soares, Data Scientist Specialist at Bayer (Crop Science)
  - marcosoares.feq@gmail.com

- Gabriel Fernandes Luz, Senior Data Scientist
  - gfluz94@gmail.com

- If you cannot install the last version from idsw package directly from PyPI using `pip install idsw`:

1. Open the terminal and:

Run:

	git clone "https://github.com/marcosoares-92/IndustrialDataScienceWorkflow" 

to clone all the files (you could also fork them).

2. Go to the directory called idsw.
3. Now, open the Python terminal and: 

Navigate to the idsw folder to run: 

	pip install .

- You can use command `cd "...\idsw"`, providing the full idsw path to navigate to it.
Alternatively, run `pip install ".\*.tar.gz"` in the folder terminal. 

### After cloning the directory, you can also run the package without installing it:
1. Copy the whole idsw folder to the working directory where your python or jupyter notebook file is saved.
- There must be an idsw folder on the python file directory.
2. In your Python file: 

Run the command or run a cell (Jupyter notebook) with:

	from idsw import *

for importing all idsw functions without the alias idsw; or:

	import idsw

to import the package with the alias idsw.
