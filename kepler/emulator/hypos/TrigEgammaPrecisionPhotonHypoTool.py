
__all__ = ['TrigEgammaPrecisionPhotonHypoTool']

from Gaugi.macros import *
from Gaugi import StatusCode
from Gaugi import Algorithm
from Gaugi import ToolSvc
from Gaugi import declareProperty

from kepler.emulator import Accept
from kepler.menu import treat_trigger_dict_type


#
# Hypo tool
#
class TrigEgammaPrecisionPhotonHypoTool( Algorithm ):

  #
  # Constructor
  #
  def __init__(self, name, **kw):

    Algorithm.__init__(self, name)
    declareProperty(self, kw, "Branch", 'trig_EF_ph_tight')

    

  #
  # Initialize method
  #
  def initialize(self):
    self.init_lock()
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept(self, context):

    ph= context.getHandler("HLT__PhotonContainer")

    if not ph.checkBody( self.Branch ):
      MSG_FATAL( self, "The branch %s is not found into the HLT photon body.", branch )


    # helper accessor function
    def getDecision( container, branch ):
      passed=False
      current = container.getPos()
      for it in container:
        if it.accept(branch):  passed=True;  break;
      container.setPos(current) # to avoid location fail
      return passed

    # Decorate the HLT electron with all final decisions
    passed =  getDecision(ph, self.Branch)

    return Accept( self.name(), [ ("Pass", passed) ] )


  #
  # Finalize method
  #
  def finalize(self):
    self.fina_lock()
    return StatusCode.SUCCESS





def configure_from_trigger( trigger ):

  d = treat_trigger_dict_type( trigger )
  pidname = d['pidname']
  name = 'Hypo__HLT__' + trigger
  emulator = ToolSvc.retrieve("Emulator")
  if not emulator.isValid(name):
    hypo = configure( name, pidname)
    emulator+=hypo

  return name


#
# Configure the hypo tool from trigger name
#
def configure( name, pidname ):
  
  from kepler.emulator import TrigEgammaPrecisionPhotonHypoTool
  hypo  = TrigEgammaPhotonHypoTool(name, Branch = 'trig_EF_ph_'+pidname )
  return hypo
