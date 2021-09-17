#!/usr/bin/env python3

from Gaugi import LoggingLevel, Logger
from Gaugi.macros import *
import argparse




class Parallel( Logger ):

  def __init__(self, fList):
    
    Logger.__init__(self)
    from Gaugi import expand_folders
    self.fList = expand_folders( fList )
    self.process_pipe = []
    self.output_stack = []
    import random
    import time
    random.seed(time.time())
    self._base_id = random.randrange(100000)
    #self._base_id = 46723

  def launch( self, _command, maxJobs ):
    import os
    import subprocess
    from pprint import pprint
    
    while len(self.fList) > 0:
      if len(self.process_pipe) < int(maxJobs):
        job_id = len(self.fList)
        f = self.fList.pop()
        oname = ('output_%d_%d.root') % (self._base_id, job_id) 
     
        run=False
        if os.path.isfile( './'+oname ):
          if (os.path.getsize( './'+oname )/float(1<<10)) < 200: # less than 2Kb
            print('This file is less than 1Kb. Should be rerun.')
            run=True
        else:
          run=True


        if run:
          self.output_stack.append( ('output_%d_%d.root') % (self._base_id, job_id) )
          command = _command+' '
          command += ('-i %s -o %s') % (f, self.output_stack[-1])
          #MSG_INFO( self,  ('adding process into the stack with id %d')%(job_id), extra={'color':'0;35'})
          MSG_INFO( self,  ('adding process into the stack with id %d')%(job_id) )
          pprint(command)
          proc = subprocess.Popen(command.split(' '))
          self.process_pipe.append( (job_id, proc) )
    
      for proc in self.process_pipe:
        if not proc[1].poll() is None:
          #MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]), extra={'color':'0;35'})
          MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]) )
          self.process_pipe.remove(proc)
    
    # Check pipe process
    # Protection for the last jobs
    while len(self.process_pipe)>0:
      for proc in self.process_pipe:
        if not proc[1].poll() is None:
          #MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]), extra={'color':'0;35'})
          MSG_INFO( self,  ('pop process id (%d) from the stack')%(proc[0]) )
          # remove proc from the pipe
          self.process_pipe.remove(proc)










mainLogger = Logger.getModuleLogger("prometheus.job")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

parser.add_argument('-i','--inputFiles', action='store', 
    dest='fList', required = True, nargs='+',
    help = "The input files.")

parser.add_argument('-c','--command', action='store', 
    dest='command', required = True,
    help = "The command job")

parser.add_argument('-mt','--numberOfThreads', action='store', 
    dest='mt', required = False, default = 8, type=int,
    help = "The number of threads")



import sys,os
if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)
args = parser.parse_args()

print (args.command)

job = Parallel(args.fList)
job.launch( args.command, args.mt)

