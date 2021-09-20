


__all__ = ['Merger','MergeFiles']


from Gaugi import Logger
from Gaugi import StatusCode
from Gaugi import expand_folders, save, load, progressbar
from Gaugi.macros import *
from pprint import pprint

import numpy as np
import pandas as pd
import gc
import re

class ReaderPool( Logger ):

  def __init__(self, fList, reader, nFilesPerJob, nthreads):

    Logger.__init__(self)
    self._fList = expand_folders( fList )
    def chunks(l, n):
      """Yield successive n-sized chunks from l."""
      for i in range(0, len(l), n):
        yield l[i:i + n]
    self._fList = [l for l in chunks(self._fList, nFilesPerJob)]
    self.process_pipe = []
    self._outputs = []
    self._nthreads = nthreads
    self._reader = reader

  def __call__( self ):
    from Gaugi import SafeProcess
    while len(self._fList) > 0:
      if len(self.process_pipe) < self._nthreads:
        job_key = len(self._fList)
        f = self._fList.pop()
        proc = SafeProcess( self._reader , job_key)
        proc(f)
        self.process_pipe.append( (job_key, proc) )

      for proc in self.process_pipe:
        if not proc[1].is_alive():
          MSG_INFO( self,  ('pop process key (%d) from the stack')%(proc[0]) )
          self._outputs.append( proc[1].get( None ))
          self.process_pipe.remove(proc)

    # Check pipe process
    # Protection for the last jobs
    while len(self.process_pipe)>0:
      for proc in self.process_pipe:
        if not proc[1].is_alive():
          MSG_INFO( self,  ('pop process key (%d) from the stack')%(proc[0]) )
          self._outputs.append( proc[1].get( None  ))
          self.process_pipe.remove(proc)

    return self._outputs



class DataReader( Logger ):

  def __init__( self, skip_these_keys,**kw ):
    Logger.__init__(self, kw)
    self._skip_these_keys = skip_these_keys


  def __call__(self, inputFiles  ):
    obj  =None
    for f in progressbar(inputFiles, 'Reading...: '):
      d = dict(np.load(f,allow_pickle=True))
      obj = self.merge(d,obj,self._skip_these_keys) if obj else d
    return obj

  @classmethod
  def merge( cls, from_dict, to_dict, skip_these_keys ):
    for key in from_dict.keys():
      if cls.skip_key(key, skip_these_keys):  continue
      if to_dict[key] is not None:
        to_dict[key] = np.concatenate( (to_dict[key], from_dict[key]) )
      else:
        to_dict[key] = from_dict[key]
    return to_dict

  @classmethod
  def skip_key( self, key, skip_these_keys ):
    for skip_this_key in skip_these_keys:
      if skip_this_key in key:
        return True
    return False






class Merger(Logger):

  def __init__( self, nthreads, **kw ):
    Logger.__init__(self, **kw)
    self._nthreads = nthreads
    self._nFilesPerJob = 1000
    self._skip_these_keys = ["features", "etBins", "etaBins", "etBinIdx","etaBinIdx","dtypes", "protocol", "allow_pickle"]
    self._pat = re.compile(r'.+(?P<binkey>et(?P<etBinidx>\d+).eta(?P<etaBinidx>\d+))\..+$')


  def __call__( self, et_bin, eta_bin, ofile, sgnFileList=None, bkgFileList=None, debug=False ):


    sgnDict=None
    bkgDict=None
    # get all keys
    key = 'et%d_eta%d'%(et_bin, eta_bin)
    if sgnFileList: 
      sgnDict = self.prepare( sgnFileList, key, debug=debug, label='Signal' )
    if bkgFileList:
      bkgDict = self.prepare( bkgFileList, key, debug=debug, label='Background' )

    data = None
    target = None
    features = None
    dtypes = None
    etbins = None
    etabins = None

    if sgnDict is None and bkgDict is None:
      return

    if sgnDict and bkgDict is None:
      data = sgnDict['pattern_'+key]
      target = np.ones( (sgnDict['pattern_'+key].shape[0],) )
      features = sgnDict['features']
      dtypes = sgnDict['dtypes']
      etbins = sgnDict['etBins']
      etabins = sgnDict['etaBins']
    elif sgnDict is None and bkgDict:
      data = bkgDict['pattern_'+key]
      target = np.ones( (bkgDict['pattern_'+key].shape[0],) )
      features = bkgDict['features']
      dtypes = bkgDict['dtypes']
      etbins = bkgDict['etBins']
      etabins = bkgDict['etaBins']
    else:
      target   = np.concatenate( ( np.ones( (sgnDict['pattern_'+key].shape[0],) ),  np.zeros( (bkgDict['pattern_'+key].shape[0],) ) ) ).astype('int16')
      data     = np.concatenate( (sgnDict['pattern_'+key], bkgDict['pattern_'+key]) )
      features = bkgDict['features']
      dtypes = bkgDict['dtypes']
      etbins = sgnDict['etBins']
      etabins = sgnDict['etaBins']

    MSG_INFO( self, "Saving: %s", ofile+'_'+key)
    self.save(data, target, features, dtypes, etbins, etabins, et_bin, eta_bin,
              ofile+'_'+key, protocol = 'savez_compressed')




  #
  # Create signal
  #
  def prepare(self, fileList, key, debug=False, label=''):
      #try:
        subFileList = []
        for f in expand_folders(fileList):
          if key in f:  subFileList.append(f)

        if debug:
          subFileList = subFileList[0:10]

        reader = ReaderPool( subFileList, DataReader(self._skip_these_keys), self._nFilesPerJob, self._nthreads )
        outputs = reader()
        d = outputs.pop()
        if len(outputs)>0:
          for from_dict in progressbar(outputs, 'Mearging %s files: '%label):
            DataReader.merge( from_dict, d, self._skip_these_keys )

        if d['pattern_'+key] is not None:
           MSG_INFO(self, label+'Data_%s : (%d, %d)', key, d['pattern_'+key].shape[0], d['pattern_'+key].shape[1])
        else:
          MSG_INFO(self, label+'Data_%s : empty', key)
        return d
      #except:
      #  return None
 

  #
  # Prepare dataset
  #
  def save( self, data, target, features, dtypes, 
            etbins, etabins, et_bin, eta_bin, ofile, protocol='savez_compressed'):

      # Loop over regions
      d = { 
            # data header
            "etBins"    : etbins,
            "etaBins"   : etabins,
            "etBinIdx"  : et_bin,
            "etaBinIdx" : eta_bin,
            }

      # Create float staff
      float_indexs = [ idx for idx, name in enumerate(dtypes) if 'float' in name]
      data_float = data[:, float_indexs  ].astype(np.float32)
      features_float = features[float_indexs]

      # create bool staff
      bool_indexs = [ idx for idx, name in enumerate(dtypes) if 'bool' in name]
      data_bool = data[:, bool_indexs  ].astype(bool)
      features_bool = features[bool_indexs]

      # create int staff
      int_indexs = [ idx for idx, name in enumerate(dtypes) if 'int' in name]
      data_int = data[:, int_indexs].astype(int)
      features_int = features[int_indexs]

      # others
      object_indexs = [ idx for idx, name in enumerate(dtypes) if 'object' in name]
      data_object = data[: , object_indexs]
      features_object = features[object_indexs]


      d['data_float'] = data_float
      d['data_bool'] = data_bool
      d['data_int'] = data_int
      d['data_object'] = data_object

      d['features_float'] = features_float
      d['features_bool'] = features_bool
      d['features_int'] = features_int
      d['features_object'] = features_object

      d['ordered_features'] = features
      d['target'] = target

      gc.collect()
      
      save(d, ofile, protocol = 'savez_compressed')




class MergeFiles(Logger):
  
  __skip_these_keys = ["features", 
                       "etBins", 
                       "etaBins", 
                       "etBinIdx",
                       "etaBinIdx",
                       "dtypes", 
                       "protocol", 
                       "allow_pickle"]

  def __init__(self, path, et_bin, eta_bin, output, sgn_part_name=None, bkg_part_name=None,
              debug = False):

    Logger.__init__(self)
    self.__files = []
    self.output = output
    self.bin_key = 'et%d_eta%d' % (et_bin, eta_bin)
    self.et_bin = et_bin
    self.eta_bin = eta_bin
    for f in expand_folders(path):
      if self.bin_key in f: self.__files.append(f)

    if debug:
      self.__files = self.__files[0::10]
    self.__sgn_part_name = sgn_part_name
    self.__bkg_part_name = bkg_part_name


  def run(self):

    d = self.merge(self.__files, self.bin_key)

    data = d['data']
    target = d['target']
    features = d['features']
    dtypes = d['dtypes']
    etbins = d['etBins']
    etabins = d['etaBins']
    
    self.save(data, target, features, dtypes, etbins, etabins)




  def merge(self, files, bin_key ):

    def skip_key( key , skip_these_keys):
      for skip_this_key in skip_these_keys:
        if skip_this_key in key:
          return True
      return False

    def merge_dict( from_dict, to_dict, skip_these_keys ):
      for key in from_dict.keys():
        if skip_key(key, skip_these_keys):  continue
        if to_dict[key] is not None:
          to_dict[key] = np.concatenate( (to_dict[key], from_dict[key]) )
        else:
          to_dict[key] = from_dict[key]
      return to_dict

    obj = None
    for f in progressbar(files, 'Reading...: '):
      d = dict(np.load(f,allow_pickle=True))
      self.prepare(f, d, bin_key )
      obj = merge_dict(d,obj,self.__skip_these_keys) if obj else d
    return obj

  
  def prepare(self, f, d, bin_key):
    d['data'] = d.pop('pattern_'+bin_key)
    n_samples = d['data'].shape[0]
    if self.__sgn_part_name in f:
      d['target'] = np.ones( (n_samples,) )
    elif self.__bkg_part_name in f:
      d['target'] = np.zeros( (n_samples,) )
  

  #
  # Prepare dataset
  #
  def save( self, data, target, features, dtypes, etbins, etabins):

      ofile = self.output+'_'+self.bin_key
      MSG_INFO(self, 'Saving... ' + ofile)
      # Loop over regions
      d = { 
            # data header
            "etBins"    : etbins,
            "etaBins"   : etabins,
            "etBinIdx"  : self.et_bin,
            "etaBinIdx" : self.eta_bin,
            }

      # Create float staff
      float_indexs = [ idx for idx, name in enumerate(dtypes) if 'float' in name]
      data_float = data[:, float_indexs  ].astype(np.float32)
      features_float = features[float_indexs]

      # create bool staff
      bool_indexs = [ idx for idx, name in enumerate(dtypes) if 'bool' in name]
      data_bool = data[:, bool_indexs  ].astype(bool)
      features_bool = features[bool_indexs]

      # create int staff
      int_indexs = [ idx for idx, name in enumerate(dtypes) if 'int' in name]
      data_int = data[:, int_indexs].astype(int)
      features_int = features[int_indexs]

      # others
      object_indexs = [ idx for idx, name in enumerate(dtypes) if 'object' in name]
      data_object = data[: , object_indexs]
      features_object = features[object_indexs]


      d['data_float'] = data_float
      d['data_bool'] = data_bool
      d['data_int'] = data_int
      d['data_object'] = data_object

      d['features_float'] = features_float
      d['features_bool'] = features_bool
      d['features_int'] = features_int
      d['features_object'] = features_object

      d['ordered_features'] = features
      d['target'] = target
      gc.collect()
      save(d, ofile, protocol = 'savez_compressed')
