
__all__ = ['EventInfo_v1']

from Gaugi import EDM
from Gaugi  import StatusCode
from kepler.core import Dataframe as DataframeEnum


class EventInfo_v1(EDM):
    __eventBranches = {
            'Electron_v1':
            [ 'RunNumber',
                'avgmu',
                'LumiBlock',
                'el_nPileupPrimaryVtx'],

            'Photon_v1':
            [ 'RunNumber',
                'avgmu',
                'LumiBlock',
                'ph_nPileupPrimaryVtx'],
            }


    def __init__(self):
        EDM.__init__(self)


    def initialize(self):
        """
          Link all branches
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            self.link( self.__eventBranches["Electron_v1"] )
            return StatusCode.SUCCESS
        elif self._dataframe is DataframeEnum.Photon_v1:
            self.link( self.__eventBranches["Photon_v1"] )
            return StatusCode.SUCCESS
        else:
            self._logger.warning("Dataframe not available.")
            return StatusCode.FAILURE

    def nvtx(self):
        """
          Retrieve the Nvtx information from Physval or SkimmedNtuple
        """
        if self._dataframe is DataframeEnum.Electron_v1:
            return self._event.el_nPileupPrimaryVtx
        elif self._dataframe is DataframeEnum.Photon_v1:
            return self._event.ph_nPileupPrimaryVtx

   
    def avgmu(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        return self._event.avgmu
        

    def RunNumber(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        return self._event.RunNumber
        

    def LumiBlock(self):
        """
          Retrieve the avgmu information from Physval or SkimmedNtuple
        """
        return self._event.LumiBlock
        

    def MCPileupWeight(self):
        """
          Retrieve the Pileup Weight information from Physval or SkimmedNtuple
        """
        return 1
        

    def id(self):
        return self._id

    def setId(self, v):
        self._id = v





