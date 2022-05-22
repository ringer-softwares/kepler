
__all__ = ['TrigElectron_v2']

from Gaugi import EDM
from Gaugi import StatusCode
import numpy as np


class TrigElectron_v2(EDM):

    __eventBranches = [
                      'trig_L2_el_pt',
                      'trig_L2_el_caloEta',
                      'trig_L2_el_eta',
                      'trig_L2_el_phi',
                      #'trig_L2_el_charge',
                      'trig_L2_el_etOverPt',
                      'trig_L2_el_trkClusDeta',
                      'trig_L2_el_trkClusDphi',
                      'trig_L2_el_trk_d0',
                    ]
                

    def __init__(self):
        EDM.__init__(self)

    def initialize(self):
        """
          Initialize all branches
        """
        self.link( self.__eventBranches )
        return StatusCode.SUCCESS
        


    def pt(self):
        """
          Retrieve the pt information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_pt[self.getPos()]
        

    def eta(self):
        """
        Retrieve the eta information from Physval or SkimmedNtuple
        """            
        return self._event.trig_L2_el_eta[self.getPos()]
        

    def phi(self):
        """
        Retrieve the phi information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_phi[self.getPos()]
      
      
    #def charge(self):
    #    """
    #     Retrieve the charge information from Physval or SkimmedNtuple
    #    """
    #    return self._event.trig_L2_el_charge[self.getPos()]
       

    def caloEta(self):
        """
        Retrieve the caloEta information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_caloEta[self.getPos()]
      

    def etOverPt(self):
        """
        Retrieve the et/pt information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_etOverPt[self.getPos()]
       

    def trkClusDeta(self):
        """
        Retrieve the trkClusDeta information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_trkClusDeta[self.getPos()]
        

    def trkClusDphi(self):
        """
        Retrieve the trkClusDphi information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_trkClusDphi[self.getPos()]
        

    def d0(self):
        """
        Retrieve the trkClusDphi information from Physval or SkimmedNtuple
        """
        return self._event.trig_L2_el_trk_d0[self.getPos()]
        


    def size(self):
        return self._event.trig_L2_el_pt.size()



    def setToBeClosestThanCluster( self ):
      idx = 0; minDeltaR = 999
      def deltaR( eta1, phi1, eta2, phi2 ):
        deta = abs( eta1 - eta2 )
        dphi = abs( phi1 - phi2 ) if abs(phi1 - phi2) < np.pi else (2*np.pi-abs(phi1-phi2))
        return np.sqrt( deta*deta + dphi*dphi )
      for trk in self:
        dR = deltaR( 0.0, 0.0, trk.trkClusDeta(), trk.trkClusDphi() )
        if dR < minDeltaR:
          minDeltaR = dR
          idx = self.getPos()
      self.setPos(idx)










