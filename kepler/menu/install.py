

__all__ =  [
              "install_commom_features_for_electron_dump",
           ]



import numpy as np
from kepler.emulator import attach
import os



def install_commom_features_for_electron_dump():

  hypos = []

  # configure L1 items
  from kepler.emulator.hypos.TrigEgammaL1CaloHypoTool import configure
  hypos = [
            configure("L1_EM3"     , "L1_EM3"     ),
            configure("L1_EM7"     , "L1_EM7"     ),
            configure("L1_EM15VH"  , "L1_EM15VH"  ),
            configure("L1_EM15VHI" , "L1_EM15VHI" ),
            configure("L1_EM20VH"  , "L1_EM20VH"  ),
            configure("L1_EM20VHI" , "L1_EM20VHI" ),
            configure("L1_EM22VH"  , "L1_EM22VH"  ),
            configure("L1_EM22VHI" , "L1_EM22VHI" ),
            configure("L1_EM24VHI" , "L1_EM24VHI" ),
  ]


  # configure T2Calo for each ET bin used to emulated the HLT only
  from kepler.emulator.hypos.TrigEgammaFastCaloHypoTool import configure
  for pidname in ['lhvloose', 'lhloose','lhmedium', 'lhtight']:
    # T2Calo
    hypos+= [
            configure('trig_L2_cl_%s_et0to12'%pidname   , 0  , pidname),
            configure('trig_L2_cl_%s_et12to22'%pidname  , 12 , pidname),
            configure('trig_L2_cl_%s_et22toInf'%pidname , 22 , pidname),
    ]


  # configure L2 electron decisions for each bin
  from kepler.emulator.hypos.TrigEgammaFastElectronHypoTool import configure
  hypos += [
            configure('trig_L2_el_cut_pt0to15'   , 0 ),
            configure('trig_L2_el_cut_pt15to20'  , 15),
            configure('trig_L2_el_cut_pt20to50'  , 20),
            configure('trig_L2_el_cut_pt50toInf' , 50),
          ]


  return attach(hypos)
