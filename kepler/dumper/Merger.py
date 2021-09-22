


__all__ = ['MergeFiles']


from Gaugi import Logger
from Gaugi import StatusCode
from Gaugi import expand_folders, save, load, progressbar
from Gaugi.macros import *
from pprint import pprint

import numpy as np
import pandas as pd
import gc
import re


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
