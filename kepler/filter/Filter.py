__all__ = ['Filter']


from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import StatusWTD # use this to stop the sequence and skip the event
from Gaugi.macros import *


#
# Event selection
#
class Filter( Algorithm ):

  #
  # Constructor
  #
  def __init__(self, name, filters = []):

    Algorithm.__init__(self, name)

    # Cut type and values
    self.__filters = filters


  #
  # Initialize method
  #
  def initialize(self):
    return StatusCode.SUCCESS

  
  #
  # Execute method
  #
  def execute(self, context):
    
    for filter in self.__filters:
      if not filter(context):
        self.wtd = StatusWTD.ENABLE
        return StatusCode.SUCCESS

    self.wtd = StatusWTD.DISABLE
    return StatusCode.SUCCESS


  #
  # Finalize method
  #
  def finalize(self):
    return StatusCode.SUCCESS






