
__all__ = ["Menu_v1"]


from Gaugi import EDM
from Gaugi import ToolSvc
from Gaugi import StatusCode
from Gaugi.macros import *

from kepler.events import AcceptType
from kepler.emulator import Accept


#
# EDM Menu
#
class Menu_v1(EDM):

  #
  # Constructor
  #
  def __init__(self):
    EDM.__init__(self)


  #
  # Initialize method
  #
  def initialize(self):

    if not ToolSvc.retrieve("Emulator"):
      MSG_FATAL( self, "The emulator tool is not in the ToolSvc" )

    return StatusCode.SUCCESS


  #
  # Execute method
  #
  def execute(self):
    MSG_DEBUG( self, "Clear all decorations..." )
    self.clearDecorations()
    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):
    return StatusCode.SUCCESS


  #
  # Accept method
  #
  def accept( self, key ):

    # is in cache?
    if key in self.decorations():
      # decision in cache
      return self.getDecor( key )

    # get the accept decision from the TDT metadata
    elif key.startswith('TDT__'):
      #  TDT__HLT__e28_lhtight_nod0_ivarloose
      #  TDT__EFCalo__e28_lhtight_nod0_ivarloose
      tdt = self.getContext().getHandler("HLT__TDT")
      trigInfo = key.split('__')
      # TDT__AcceptType__trigItem
      passed = tdt.ancestorPassed( 'HLT_'+trigInfo[-1], AcceptType.fromstring(trigInfo[1]) )
      accept = Accept( key )
      accept.setCutResult( 'Pass', passed )
      self.setDecor( key, accept )
      return accept


    # This name is not in metadata and not in cache, let's access the emulation svc and run it!
    else:
      emulator = ToolSvc.retrieve( "Emulator" )

      if emulator.isValid( key ):
        accept = emulator.accept( self.getContext(), key )
        self.setDecor( key, accept )
        return accept
      else:
        MSG_FATAL( self, "It's is not possble to interpreter the key: %s.", key )


