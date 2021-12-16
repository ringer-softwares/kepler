
__all__ = ["TrigEgammaFastCaloRingerHypoTool", "RingerSelectorTool", "load_ringer_models"]

from Gaugi.macros import *
from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import GeV
from Gaugi import ToolSvc
from Gaugi import declareProperty

from kepler.menu import treat_trigger_dict_type
from kepler.emulator import Accept
from kepler.utils import get_bin_indexs
from tensorflow.keras.models import model_from_json

import numpy as np
import os 

os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


#
# generic ringer hypo tool
#
class RingerSelectorTool(Algorithm):

  #
  # Constructor
  #
  def __init__(self, name, generator ,**kw  ):

    Algorithm.__init__(self, name)

    declareProperty(self, kw, "ConfigFile" , None)
    declareProperty(self, kw, "Generator"  , None)



  #
  # Inialize the selector
  #
  def initialize(self):

    if not self.ConfigPath:
      MSG_FATAL(self, "You shoul pass some path to config path property.")
    self.__tuning, version = load_ringer_models(self.ConfigPath)
    MSG_INFO( self, "Tuning version: %s" , version )
    MSG_INFO( self, "Loaded %d models for inference." , len(self.__model))
    MSG_INFO( self, "Loaded %d threshold for decision" , len(self.__tuning))

    return StatusCode.SUCCESS



  def accept( self, context):

    accept = Accept(self.name(), [('Pass', False)])
    accept.setDecor( "discriminant",-999 )
    fc = context.getHandler("HLT__TrigEMClusterContainer")
    eventInfo = context.getHandler( "EventInfoContainer" )
    avgmu = eventInfo.avgmu()

    eta = abs(fc.eta())
    if eta>2.5: eta=2.5
    et = fc.et()/GeV # in GeV

    etBinIdx, etaBinIdx = get_bin_indexs( et, eta, self.__tuning['model_etBins'], 
                                          self.__tuning['model_etaBins'], logger=self._logger )
    # If not fount, return false
    if etBinIdx < 0 or etaBinIdx < 0:
      return accept

    # get the model for inference
    model = self.__tuning['models'][etBinIdx][etaBinIdx]

    etBinIdx, etaBinIdx = get_bin_indexs( et, eta, self.__tuning['threshold_etBins'], 
                                          self.__tuning['threshold_etaBins'], logger=self._logger )
    # If not fount, return false
    if etBinIdx < 0 or etaBinIdx < 0:
      return accept

    # get the threshold
    cut = self.__tuning['thresholds'][etBinIdx][etaBinIdx]



    # Until here, we have all to run it!
    data = self.Generator( context )
    # compute the output
    if data:
      output = model.predict( data )[0][0].numpy()
    else:
      return accept

    accept.setDecor("discriminant", output)

    # If the output is below of the cut, reprove it
    if output <= (cut['slope']*avgmu + cut['offset']):
      return accept

    # If arrive until here, so the event was passed by the ringer
    accept.setCutResult( "Pass", True )
    return accept






#
# Load all ringer models from athena format
#
def load_ringer_models( configPath ):
    

    basepath = '/'.join(configPath.split('/')[:-1])
    from ROOT import TEnv
    env = TEnv( configPath )
    version = env.GetValue("__version__", '')

    def treat_float( env, key ):
      return [float(value) for value in  env.GetValue(key, '').split('; ')]

    def treat_string( env, key ):
      return [str(value) for value in  env.GetValue(key, '').split('; ')]

    #
    # Reading all models
    #
    number_of_models = env.GetValue("Model__size", 0)
    etmin_list = treat_float( env, 'Model__etmin' )
    etmax_list = treat_float( env, 'Model__etmax' )
    etamin_list = treat_float( env, 'Model__etamin' )
    etamax_list = treat_float( env, 'Model__etamax' )
    paths = treat_string( env, 'Model__path' )
    
    #
    # deserialize list to matrix
    #
    etbins = np.unique(etmin_list).tolist()
    etbins.append(etmax_list[-1])
    etabins = np.unique(etamin_list).tolist()
    etabins.append(etamax_list[-1])

    d = {
            'models' : [ [None for _ in range(len(etabins)-1)] for __ in range(len(etbins)-1) ],
            'model_etBins' : etbins, 
            'model_etaBins': etabins, 
        }

    etBinIdx=0
    etaBinIdx=0
    for idx, path in enumerate( paths ):
      if etaBinIdx > len(etabins)-2:
        etBinIdx +=1
        etaBinIdx = 0 
      path = basepath+'/'+path.replace('.onnx','')
      with open(path+'.json', 'r') as json_file:
          model = model_from_json(json_file.read())
          # load weights into new model
          model.load_weights(path+".h5")
          d['models'][etBinIdx][etaBinIdx] = model
      etaBinIdx+=1

    #
    # Reading all thresholds
    #  
   
    number_of_thresholds = env.GetValue("Threshold__size", 0)
    max_avgmu = treat_float( env, "Threshold__MaxAverageMu" )
    try:
      min_avgmu = treat_float( env, "Threshold__MinAverageMu" )
    except: # NOTE: this should be remove for future
      min_avgmu = [16]*len(number_of_thresholds)
    etmin_list = treat_float( env, 'Threshold__etmin' )
    etmax_list = treat_float( env, 'Threshold__etmax' )
    etamin_list = treat_float( env, 'Threshold__etamin' )
    etamax_list = treat_float( env, 'Threshold__etamax' )
    slopes = treat_float( env, 'Threshold__slope' )
    offsets = treat_float( env, 'Threshold__offset' )

    #
    # deserialize list to matrix
    #

    etbins = np.unique(etmin_list).tolist()
    etbins.append(etmax_list[-1])
    etabins = np.unique(etamin_list).tolist()
    etabins.append(etamax_list[-1])
    
    d['thresholds'] = [ [None for _ in range(len(etabins)-1)] for __ in range(len(etbins)-1) ]
    d['threshold_etBins'] = etbins
    d['threshold_etaBins'] = etabins
    
    etBinIdx=0
    etaBinIdx=0
    for idx, slope in enumerate(slopes):
      if etaBinIdx > len(etabins)-2:
        etBinIdx +=1
        etaBinIdx = 0 
      d['thresholds'][etBinIdx][etaBinIdx] = {'slope':slope, 'offset':offsets[idx] , 'min_avgmu': min_avgmu[idx], 'max_avgmu': max_avgmu[idx]}
      etaBinIdx+=1

    return d, version


#
# FastCalo hypo 
#
class TrigEgammaFastCaloRingerHypoTool(RingerSelectorTool):
  def __init__(self, name, generator, **kw):
    RingerSelectorTool.__init__(name, generator, **kw)

