class LoadIDSW:
  """Load IndustrialDataScienceWorkflow on your environment without installing with pip install."""

  def __init__(self, timeout = 60):
    """
      DEFINE COMMANDS (Bash script) and success messages and set timeout.
      : param: timeout (int): number of seconds to wait for a command to run, before considering error.
    """
    # Clone git repository:
    self.cmd_line1 = """git clone https://github.com/marcosoares-92/IndustrialDataScienceWorkflow IndustrialDataScienceWorkflow"""
    self.msg1 = "Cloning IndustrialDataScienceWorkflow to working directory."

    # Move idsw directory to root (Python workspace):
    self.cmd_line2 = """mv IndustrialDataScienceWorkflow/idsw ."""
    self.msg2 = "Subdirectory 'idsw' moved to root directory. Now it can be directly imported."

    self.timeout = timeout
  

  def set_process (self, cmd_line):
    """Define a process to run from a command:
    : param: cmd_line (str): command that is passed to a command line interface.
      Attention: different parts and flags must be separated by single whitespaces.
    """
    from subprocess import Popen, PIPE, TimeoutExpired

    proc = Popen(cmd_line.split(" "), stdout = PIPE, stderr = PIPE)
    """cmd_line = "git clone https://github.com/marcosoares-92/IndustrialDataScienceWorkflow IndustrialDataScienceWorkflow"
      will lead to the list ['git', 'clone', 'https://github.com/marcosoares-92/IndustrialDataScienceWorkflow', 'IndustrialDataScienceWorkflow']
      after splitting the string in whitespaces, what is done by .split(" ") method.
    """
    return proc
  

  def run_process (self, proc, msg = ''):
    """Run process defined by method set_process.
      : param: proc: process execution object returned from set_process.
      : param: msg (str): user-defined confirmation method.
      : param: timeout (int): number of seconds to wait for a command to run, before considering error.
    """

    try:
        output, error = proc.communicate(timeout = self.timeout)
        if len(msg > 0):
          print (msg)
    except:
        # General exception
        output, error = proc.communicate()
        
    return output, error


  def clone_repo(self):
    """Clone GitHub Repository."""
    
    # SET PROCESS:
    self.proc1 = self.set_process (self.cmd_line1)
    # RUN PROCESS:
    self.output1, self.error1 = self.run_process(self.proc1, self.msg1)

    return self

  
  def move_pkg(self):
    """Move package to the working directory, to make it available."""
    
    # SET PROCESS:
    self.proc2 = self.set_process (self.cmd_line2)
    # RUN PROCESS:
    self.output2, self.error2 = self.run_process(self.proc2, self.msg2)

    return self
  

  def move_pkg_alternative(self):
    """Alternative using the Bash utils module (shutil)"""
    # importing shutil module  
    import shutil
    
    # Source path  
    source = 'IndustrialDataScienceWorkflow/idsw'  
    # Destination path  
    destination = '.'
    # Move the content of source to destination  
    dest = shutil.move(source, destination)
    
    return self


loader = LoadIDSW(timeout = 60)
loader = loader.clone_repo()
loader = loader.move_pkg()

try:
  from idsw import *
except ModuleNotFoundError:
  # Package was not moved.
  loader = loader.move_pkg_alternative()

msg = """Package copied to the working directory.
To import its whole content, run:

    from idsw import *
"""
print(msg)
