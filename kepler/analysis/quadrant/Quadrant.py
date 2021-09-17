__all__ = ["Quadrant"]


from Gaugi import GeV
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import StoreGate
from Gaugi import Logger
from Gaugi.macros import *


from kepler.analysis.constants import offline_etbins, offline_etabins, var_config, mubins
from kepler.analysis.efficiency.utils import FillHistogram
from ROOT import TH1F, TH2F

import numpy as np
import array


#
# Quadrant
#
class Quadrant( Logger ):
  
  __quadrants = [ 'passed_passed', 'passed_rejected', 'rejected_passed', 'rejected_rejected']

  #
  # Constructor
  #
  def __init__(self, output, etbins  = offline_etbins, etabins = offline_etabins , 
                             mubins = mubins , combinations = []):

    Logger.__init__(self)

    self.pairs = []
    self.etbins = array.array('d',etbins) if not type(etbins) is array.array else etbins
    self.etabins = array.array('d',etabins) if not type(etabins) is array.array else etabins
    self.mubins = array.array('d',mubins) if not type(mubins) is array.array else mubins

    if type(output) is str: # We should create a new store gate
      MSG_INFO(self, "Creating the StoreGate service with path: %s", output)
      self.__store = StoreGate(output)
      for trigger_chain0, trigger_chain1 in combinations:
        self.book(trigger_chain0, trigger_chain1)
    elif type(output) is StoreGate: # Using an external store gate
      self.__store = output
    else:
      MSG_FATAL(self, "Output type should be a str (path) or the StoreGate object.")


  def __del__(self):
    self.store().write()
    

  #
  # Get the store gate service
  #
  def store(self):
    return self.__store


  def save(self):
    self.__store.write()


  #
  # Initialize
  #
  def book(self, trigger_chain0, trigger_chain1 ):

    sg = self.store()
    name = trigger_chain0 + '_and_' + trigger_chain1

    for et_bin in range(len(self.etbins)-1):
      ### loop over etas...
      for eta_bin in range(len(self.etabins)-1):
        ### loop over quadrants...
        for quadrant in self.__quadrants:  
          # hold binning name
          bin_key = ('et%d_eta%d') % (et_bin,eta_bin)
          path = name + '/' + bin_key + '/' + quadrant
          sg.mkdir( path )

          for var, tname, bins in zip(['et','eta','avgmu'], ['#E_{T}', '#eta', '<#mu>'],
                                 [self.etbins, self.etabins, self.mubins]):
            sg.addHistogram(TH1F(var, '%s;%s;Count'% (tname,tname), len(bins)-1, bins ) )

          for key, var in var_config.items():
            sg.addHistogram(TH1F(key,('%s;%s;Count')%(var['xlabel'],var['xlabel']),var['nbins'],var['edges'][0],var['edges'][1]))

    self.pairs.append( trigger_chain0 + '_and_' + trigger_chain1 )

  #
  #
  #
  def fill( self, df, trigger_chain0, trigger_chain1, pidname ):

    name = trigger_chain0 + '_and_' + trigger_chain1
    if not name in self.pairs:
      self.book( trigger_chain0, trigger_chain1 )

    sg = self.store()

    for et_bin in range(len(self.etbins)-1):
      for eta_bin in range(len(self.etabins)-1):

        etmin = self.etbins[et_bin] * GeV
        etmax = self.etbins[et_bin+1] * GeV
        etamin = self.etabins[eta_bin]
        etamax = self.etabins[eta_bin+1]

        bin_key = 'et%d_eta%d' % (et_bin, eta_bin)

        for idx, (chain0_answer, chain1_answer) in enumerate([(True,True),(True,False),(False,True),(False,False)]):

          quadrant = self.__quadrants[idx]
          df_temp = df.loc[ (df[trigger_chain0]==chain0_answer) & (df[trigger_chain1]==chain1_answer) & \
                            (df['el_et'] >= etmin) & (df['el_et'] < etmax) & \
                            (abs(df['el_eta']) >= etamin) & (abs(df['el_eta']) < etamax) &
                            (df[pidname] == True)]

          if df_temp.shape[0] > 0:
            for var in var_config.keys():
              FillHistogram( sg.histogram(name+'/'+bin_key+'/'+quadrant+'/'+var), df_temp['el_'+var].values )




   
