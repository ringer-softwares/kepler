
__all__ = ['EmTauRoI_v1']

from Gaugi import EDM
from Gaugi import StatusCode
from Gaugi import stdvector2list
from kepler.core import Dataframe as DataframeEnum


class EmTauRoI_v1(EDM):

    __eventBranches = [
                'trig_L1_eta',
                'trig_L1_phi',
                'trig_L1_emClus',
                'trig_L1_tauClus',
                'trig_L1_emIsol',
                'trig_L1_hadIsol',
                ]


    def __init__(self):
        EDM.__init__(self)


    def initialize(self):
      """
        Link all branches
      """
      self.link(self.__eventBranches)
      return StatusCode.SUCCESS
      

    def emClus(self):
        """
          Retrieve the L1 EmClus information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_emClus
        

    def tauClus(self):
        """
          Retrieve the L1 tauClus information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_tauClus
       

    def emIsol(self):
        """
          Retrieve the L1 emIsol information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_emIsol
   

    def hadCore(self):
        """
          Retrieve the L1 hadIsol information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_hadIsol
      

    def eta(self):
        """
          Retrieve the eta information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_eta
    

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        return self._event.trig_L1_phi
     




