
__all__ = ['MonteCarlo_v2']

from Gaugi import EDM
from Gaugi import StatusCode


class MonteCarlo_v2(EDM):

  __eventBranches = [ # For electron and photon
                      'mc_hasMC',
                      'mc_isTruthElectronAny',
                      'mc_isTruthElectronFromZ',
                      #'mc_isTruthElectronFromW',
                      'mc_isTruthElectronFromJpsiPrompt',
                      #'mc_isTruthJetFromAny',
                      #'mc_isTruthPhotonFromAny',
                      'mc_type',
                      'mc_origin',
                    ]


  def __init__(self):
    EDM.__init__(self)



  def initialize(self):
    """
    Initialize all branches
    """
    self.link( self.__eventBranches )
    return StatusCode.SUCCESS


  def isTruthElectronFromZ(self):
    return self._event.mc_isTruthElectronFromZ
   

  def isTruthElectronFromW(self):
    return self._event.mc_isTruthElectronFromW
    

  def isTruthElectronFromJpsiPrompt(self):
    return self._event.mc_isTruthElectronFromJpsiPrompt
   

  def isTruthElectronFromAny(self):
    return self._event.mc_isTruthElectronAny
    

  def isTruthJetFromAny(self):
    return self._event.mc_isTruthJetFromAny
   

  def isTruthPhotonFromAny(self):
    return self._event.mc_isTruthPhotonFromAny
   
  
  def isMC(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    return bool(self._event.mc_hasMC)
   

  def type(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    return self._event.mc_type
    

  def origin(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    return self._event.mc_origin
    


