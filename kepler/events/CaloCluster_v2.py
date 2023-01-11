
__all__ = ["CaloCluster_v2"]


from Gaugi import EDM
from Gaugi import StatusCode
from kepler.core import Dataframe as DataframeEnum
import numpy as np

class CaloCluster_v2(EDM):

  # define all skimmed branches here.
  __eventBranches = {
                  'CaloCluster':[
                              'el_calo_et',
                              'el_calo_eta',
                              'el_calo_phi',
                              'el_calo_etaBE2',
                              'el_calo_e',
                            ],
                   'HLT__CaloCluster':[
                              'trig_EF_calo_e',
                              'trig_EF_calo_et',
                              'trig_EF_calo_eta',
                              'trig_EF_calo_phi',
                              'trig_EF_calo_etaBE2',
                             
                              ]
                    }



  def __init__(self):
    EDM.__init__(self)


  def initialize(self):

    self.link( self.__eventBranches['HLT__CaloCluster'] if self._is_hlt else self.__eventBranches["CaloCluster"] )
   

    return StatusCode.SUCCESS


  def et(self):
    """
      Retrieve the Et information from Physval or SkimmedNtuple
    """
    if self._is_hlt:
      return self._event.trig_EF_calo_et[self.getPos()]
    else:
      return self._event.el_calo_et
   


  def eta(self):
    """
      Retrieve the Eta information from Physval or SkimmedNtuple
    """
    if self._is_hlt:
      return self._event.trig_EF_calo_eta[self.getPos()]
    else:
      return self._event.el_calo_eta



  def phi(self):
    """
      Retrieve the Phi information from Physval or SkimmedNtuple
    """
    if self._is_hlt:
      return self._event.trig_EF_calo_phi[self.getPos()]
    else:
      return self._event.el_calo_phi


  def etaBE2(self):
    """
      Retrieve the EtaBE2 information from Physval or SkimmedNtuple
    """
    if self._is_hlt:
      return self._event.trig_EF_calo_etaBE2[self.getPos()]
    else:
      return self._event.el_calo_etaBE2


  def energy(self):
    """
      Retrieve the E information from Physval or SkimmedNtuple
    """
    if self._is_hlt:
      return self._event.trig_EF_calo_e[self.getPos()]
    else:
      return self._event.el_calo_e



  def emCluster(self):
    """
      Retrieve the TrigEmCluster (FastCalo) python object into the Store Event
      For now, this is only available into the PhysVal dataframe.
    """
    cluster = self.getContext().getHandler('HLT__TrigEMClusterContainer')
    cluster.setPos(self.getPos())
    return cluster




  def size(self):
    """
    	Retrieve the TrackParticle container size
    """
    if self._is_hlt:
      return self.event.trig_EF_calo_eta.size()
    else:
      return 1
    


  def empty(self):
    return False if self.size()>0 else True




  def setToBeClosestThan( self, eta, phi ):
    found=False
    idx = self.getPos(); minDeltaR = 999
    def deltaR(  eta1, phi1, eta2, phi2 ):
      deta = abs( eta1 - eta2 )
      dphi = abs( phi1 - phi2 ) if abs(phi1 - phi2) < np.pi else (2*np.pi-abs(phi1-phi2))
      return np.sqrt( deta*deta + dphi*dphi )
    for cl in self:
      dR = deltaR( eta, phi, cl.eta(), cl.phi() )
      if dR>0.07:
        continue
      if dR < minDeltaR:
        minDeltaR = dR
        idx = cl.getPos()
        found=True
    self.setPos(idx)
    return found