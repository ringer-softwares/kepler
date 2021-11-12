


__all__ = ["MergeNpz", "MergeNpzPool"]


from Gaugi import LoggingLevel, Logger, ensure_extension
from Gaugi import expand_folders, save, load, progressbar
from Gaugi.macros import *
from Gaugi import Slot
from pprint import pprint

import numpy as np
import sys,os

import time

#
# Merge npz files
#
class MergeNpz(Logger):

  def __init__(self , merge_these_keys ):
    self.__merge_these_keys = merge_these_keys
    self.__pop_these_keys = ['allow_pickle', 'protocol']

  def run( self, files , output):

    output = ensure_extension(output,'npz')

    if len(files) == 1:
      d = load(files[0])
      for key in self.__pop_these_keys:
        d.pop(key)
      save(d, output, protocol = 'savez_compressed')
    else:
      # load the first
      d = load( files.pop() )
      for filename in progressbar(files):
        self.merge( filename, d )

      for key in self.__pop_these_keys:
          d.pop(key)
        
      # Save the merged file!
      save(d, output, protocol = 'savez_compressed')

  def merge( self, filename, to_dict ):
    from_dict = load( filename )
    for key in to_dict.keys():
      if key in self.__merge_these_keys:
        to_dict[key] = np.concatenate( (to_dict[key],from_dict[key]) ) 



class MergeNpzPool( Logger ):

  def __init__(self, files, output, maxFilesPerJob, maxJobs ):
    
    Logger.__init__(self)

    self.files = expand_folders( files )
    self.output = output
    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
        yield l[i:i + n]
    f = []
    for l in chunks(self.files, maxFilesPerJob):
      f.append(l)
    self.__files_per_job= f
    self.__slots = [Slot() for _ in range(maxJobs)]
    self.__outputs = []


  def getAvailable(self):
    for slot in self.__slots:
      if slot.isAvailable():
        return slot
    return None

  
  def busy(self):
    for slot in self.__slots:
      if not slot.isAvailable():
        return True
    return False


  def generate(self):
    files = self.__files_per_job.pop()
    idx = len(self.__files_per_job)
    output = self.output + '.' + str(idx) + '.npz'
    self.__outputs.append(output)
    command = 'merge_npz.py -f '
    for f in files:
      command += f + ' '
    command += '-o ' + output
    return command


  def run( self ):
    while len(self.__files_per_job) > 0:

      #for idx, s in enumerate(self.__slots):
      #  print(str(idx) + ' ' + str(s.isAvailable()) )

      slot = self.getAvailable()
      if slot:
        #time.sleep(1)
        command = self.generate()
        slot.run( command )
    while self.busy():
      continue

    if len(self.__outputs) > 1:
      self.merge()
    else:
      os.system('mv ' +self.__outputs[0] + ' ' + ensure_extension(self.output, 'npz') )



  def merge(self):
    command = "merge_npz.py -f "
    for fname in self.__outputs:
      command += fname + ' '
    command += '-o ' + self.output
    os.system(command)
    for fname in self.__outputs:
      os.system( 'rm -rf '+fname)


