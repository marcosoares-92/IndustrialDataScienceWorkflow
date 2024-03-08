# Industrial Data Science Workflow
## Industrial Data Science Workflow: full workflow for ETL, statistics, and Machine learning modelling of (usually) time-stamped industrial facilities data.
### Not only applicable to monitoring quality and industrial facilities systems, the package can be applied to data manipulation, characterization and modelling of different numeric and categorical datasets to boost your work and replace tradicional tools like SAS, Minitab and Statistica software.

- Check the project Github: https://github.com/marcosoares-92/IndustrialDataScienceWorkflow
- Check our `Steel Industry Simulator` on: https://github.com/marcosoares-92/steelindustrysimulator
	- The Ideal Tool for Process Improvement, and Data Collection, Analyzing and Modelling Training.
	- User interface available in: 
	
	https://colab.research.google.com/github/marcosoares-92/steelindustrysimulator/blob/main/steelindustry_digitaltwin.ipynb


Authors:
- Marco Cesar Prado Soares, Data Scientist Specialist at Bayer (Crop Science)
  - marcosoares.feq@gmail.com

- Gabriel Fernandes Luz, Senior Data Scientist
  - gfluz94@gmail.com

- Sergio Guilherme Neto, Data Analyst
  - sguilhermeneto@gmail.com

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

### Alternatively, if you do not want to clone the repository, you may download the file `load.py` and copy it to the working directory.
1. After downloading load.py and copying it to the working directory, in your Python environment, run:
	
	import load

2. After conclusion of this step, you may import the package as:

	from idsw import *

or as:
	
	import idsw

#### The `load.py` file runs the following code, which may be copied to your Python environment and run:

	class LoadIDSW:

	  def __init__(self, timeout = 60):  
	    self.cmd_line1 = """git clone https://github.com/marcosoares-92/IndustrialDataScienceWorkflow IndustrialDataScienceWorkflow"""
	    self.msg1 = "Cloning IndustrialDataScienceWorkflow to working directory."
	    self.cmd_line2 = """mv IndustrialDataScienceWorkflow/idsw ."""
	    self.msg2 = "Subdirectory 'idsw' moved to root directory. Now it can be directly imported."
	    self.timeout = timeout

  	  def set_process (self, cmd_line):
	    from subprocess import Popen, PIPE, TimeoutExpired
	    proc = Popen(cmd_line.split(" "), stdout = PIPE, stderr = PIPE)
	    return proc

	  def run_process (self, proc, msg = ''):
	    try:
	        output, error = proc.communicate(timeout = self.timeout)
	        if len(msg > 0):
	          print (msg)
	    except:
	        output, error = proc.communicate()       
	    return output, error

	  def clone_repo(self):
	    self.proc1 = self.set_process (self.cmd_line1)
	    self.output1, self.error1 = self.run_process(self.proc1, self.msg1)
	    return self

	  def move_pkg(self):
	    self.proc2 = self.set_process (self.cmd_line2)
	    self.output2, self.error2 = self.run_process(self.proc2, self.msg2)
	    return self

	  def move_pkg_alternative(self):
	    import shutil
	    source = 'IndustrialDataScienceWorkflow/idsw'  
	    destination = '.'
	    dest = shutil.move(source, destination)    
	    return self

	loader = LoadIDSW(timeout = 60)
	loader = loader.clone_repo()
	loader = loader.move_pkg()

	try:
	  from idsw import *
	except ModuleNotFoundError:
	  loader = loader.move_pkg_alternative()

	msg = """Package copied to the working directory.
		To import its whole content, run:
		
		    from idsw import *
		"""
	print(msg)