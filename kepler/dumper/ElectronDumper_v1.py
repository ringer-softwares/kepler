
__all__ = ["ElectronDumper_v1"]


from Gaugi import Algorithm
from Gaugi import StatusCode
from Gaugi import save, declareProperty
from Gaugi.macros import *


from kepler.core import Dataframe as DataframeEnum 
from kepler.events import EgammaParameters
from kepler.utils import get_bin_indexs


import numpy as np
import collections
import gc



#
# Electron
#
class ElectronDumper_v1( Algorithm ):


  #
  # constructor
  #
  def __init__(self, output, etbins, etabins, target, **kw ):
    
    Algorithm.__init__(self, "")

    declareProperty( self, kw, 'dumpRings', True)

    self.__target = target
    self.__etbins = etbins
    self.__etabins = etabins
    self.__outputname = output

    self.__event = {}
    self.__event_label = []
    self.__decorators = collections.OrderedDict({})
    self.__save_these_bins = list()
    self.__extra_features = list()


 
  def __add__( self, key ):
    if type(key) is str:
      key = [key]
    self.__extra_features.extend( key )
    return self


  def decorate( self, key , f):
    self.__decorators[key] = f


  #
  # Initialize dumper
  #
  def initialize(self):

    Algorithm.initialize(self)

    # build map
    for etBinIdx in range(len(self.__etbins)-1):
      for etaBinIdx in range(len(self.__etabins)-1):
        self.__event[ 'et%d_eta%d' % (etBinIdx,etaBinIdx) ] = None

    #
    # Event info
    #
    self.__event_label.extend( ['RunNumber', 'avgmu'] )

    #
    # Fast calo
    #
    self.__event_label.extend( [
                                'trig_L2_cl_et',
                                'trig_L2_cl_eta',
                                'trig_L2_cl_phi',
                                'trig_L2_cl_reta',
                                'trig_L2_cl_ehad1', 
                                'trig_L2_cl_eratio',
                                'trig_L2_cl_f1', 
                                'trig_L2_cl_f3', 
                                'trig_L2_cl_weta2', 
                                'trig_L2_cl_wstot', 
                                'trig_L2_cl_e2tsts1'] )

    # Add fast calo ringsE
    if self.dumpRings:
      self.__event_label.extend( [ 'trig_L2_cl_ring_%d'%r for r in range(100) ] )


    #
    # Fast electron
    #
    self.__event_label.extend( [
                                'trig_L2_el_hastrack',
                                'trig_L2_el_pt',
                                'trig_L2_el_eta',
                                'trig_L2_el_phi',
                                'trig_L2_el_caloEta',
                                'trig_L2_el_trkClusDeta',
                                'trig_L2_el_trkClusDphi',
                                'trig_L2_el_etOverPt'] )

    #
    # Calo cluster
    #
    self.__event_label.extend( [
                                'trig_EF_cl_hascluster',
                                'trig_EF_cl_et',
                                'trig_EF_cl_eta',
                                'trig_EF_cl_etaBE2',
                                'trig_EF_cl_phi',
                                ] )

    #
    # HLT electron
    #
    self.__event_label.extend( [       
                                'trig_EF_el_hascand',
                                'trig_EF_el_et',
                                'trig_EF_el_eta',
                                'trig_EF_el_etaBE2',
                                'trig_EF_el_phi',
                                'trig_EF_el_rhad1',
                                'trig_EF_el_rhad',
                                'trig_EF_el_f3',
                                'trig_EF_el_weta2',
                                'trig_EF_el_rphi',
                                'trig_EF_el_reta',
                                'trig_EF_el_wtots1',
                                'trig_EF_el_eratio',
                                'trig_EF_el_f1',
                                'trig_EF_el_hastrack',
                                'trig_EF_el_deltaEta1',
                                'trig_EF_el_deltaPhi2',
                                'trig_EF_el_deltaPhi2Rescaled',
                                'trig_EF_el_lhtight',
                                'trig_EF_el_lhmedium',
                                'trig_EF_el_lhloose',
                                'trig_EF_el_lhvloose', 
                                ] )


    #
    # Offline variables
    #
    self.__event_label.extend( [
                                # Offline variables
                                'el_et',
                                'el_eta',
                                'el_etaBE2',
                                'el_phi',
                                # offline shower shapers
                                'el_rhad1',
                                'el_rhad',
                                'el_f3',
                                'el_weta2',
                                'el_rphi',
                                'el_reta',
                                'el_wtots1',
                                'el_eratio',
                                'el_f1',
                                # offline track
                                'el_hastrack',
                                'el_numberOfBLayerHits',
                                'el_numberOfPixelHits',
                                'el_numberOfTRTHits',
                                'el_d0',
                                'el_d0significance',
                                'el_eProbabilityHT',
                                'el_trans_TRT_PID',
                                'el_deltaEta1',
                                'el_deltaPhi2',
                                'el_deltaPhi2Rescaled',
                                'el_deltaPOverP',
                                'el_lhtight',
                                'el_lhmedium',
                                'el_lhloose',
                                'el_lhvloose',
                                ] )


    self.__event_label.extend( self.__decorators.keys() )

    self.__event_label.extend( self.__extra_features )

    return StatusCode.SUCCESS


  #
  # fill current event
  #
  def fill( self, key , event ):

    if self.__event[key]:
      self.__event[key].append( event )
    else:
      self.__event[key] = [event]


  #
  # execute 
  #
  def execute(self, context):

    event_row = list()

    #
    # event info
    #
    eventInfo = context.getHandler( "EventInfoContainer" )
    event_row.append( eventInfo.RunNumber() )
    event_row.append( eventInfo.avgmu() )


    #
    # Fast Calo features
    #
    fc = context.getHandler( "HLT__TrigEMClusterContainer" )

    etBinIdx, etaBinIdx = get_bin_indexs( fc.et()/1000., abs(fc.eta()), self.__etbins, self.__etabins, logger=self._logger )
    if etBinIdx < 0 or etaBinIdx < 0:
      return StatusCode.SUCCESS


    event_row.append( fc.et()       )
    event_row.append( fc.eta()      )
    event_row.append( fc.phi()      )
    event_row.append( fc.reta()     )
    event_row.append( fc.ehad1()    )
    event_row.append( fc.eratio()   )
    event_row.append( fc.f1()       )
    event_row.append( fc.f3()       )
    event_row.append( fc.weta2()    )
    event_row.append( fc.wstot()    )
    event_row.append( fc.e2tsts1()  )

    if self.dumpRings:
      event_row.extend( fc.ringsE() )
   
    #
    # Fast electron features
    #
    # Save only the closest fast track object cluster-trk
    fcElCont = context.getHandler("HLT__TrigElectronContainer" )
    hasFcTrack = True if fcElCont.size()>0 else False
    if hasFcTrack:
      fcElCont.setToBeClosestThanCluster()
      event_row.append( True )
      event_row.append( fcElCont.pt() )
      event_row.append( fcElCont.eta() )
      event_row.append( fcElCont.phi() )
      event_row.append( fcElCont.caloEta() )
      event_row.append( fcElCont.trkClusDeta() )  
      event_row.append( fcElCont.trkClusDphi() )
      event_row.append( fcElCont.etOverPt() )
    else:
      event_row.extend( [False, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0] )


    # Precision step
    # NOTE: Should be closest than offline object
    elCont = context.getHandler( "ElectronContainer" )



    #
    # Calo Cluster
    #
    # get the closest online-offline object
    clCont = context.getHandler("HLT__CaloClusterContainer")
    hasCluster = True if clCont.size()>0 else False
    if hasCluster:
      clCont.setToBeClosestThan( elCont.eta(), elCont.phi() )
      event_row.append( True )
      event_row.append( clCont.et() )
      event_row.append( clCont.eta() )
      event_row.append( clCont.etaBE2() )
      event_row.append( clCont.phi() )
    else:
      event_row.extend( [False, -1.0, -1.0, -1.0, -1.0] )


    
    #
    # HLT electron
    #
    on_elCont = context.getHandler("HLT__ElectronContainer")
    hasCand = True if on_elCont.size()>0 else False
    if hasCand:
      on_elCont.setToBeClosestThan( elCont.eta(), elCont.phi() )
      event_row.append( True ) #FIXME!
      # Offline Shower shapes
      event_row.append( on_elCont.et() )
      event_row.append( on_elCont.eta() )
      event_row.append( on_elCont.caloCluster().etaBE2())
      event_row.append( on_elCont.phi() )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.Rhad1 ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.Rhad ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.f3 ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.weta2 ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.Rphi ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.Reta ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.wtots1 ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.Eratio ) )
      event_row.append( on_elCont.showerShapeValue( EgammaParameters.f1 ) )

      trkCont  = elCont.trackParticle()
      if trkCont:
        event_row.append( True ) #FIXME
        event_row.append( elCont.deta1() )
        event_row.append( elCont.dphi2() )
        event_row.append( elCont.deltaPhiRescaled2() )
      else:
        event_row.append( [False, -1.0, -1.0, -1.0] )


      # Adding PID LH decisions for each WP
      event_row.append( on_elCont.accept("trig_EF_el_lhtight")  )
      event_row.append( on_elCont.accept("trig_EF_el_lhmedium") )
      event_row.append( on_elCont.accept("trig_EF_el_lhloose")  )
      event_row.append( on_elCont.accept("trig_EF_el_lhvloose") )

    else:
      event_row.extend( [False, -1.0, -1.0, -1.0, -1.0, -1.0, 
                         -1.0, -1.0, -1.0, -1.0, -1.0, -1.0,
                         -1.0, -1.0, False, -1.0, -1.0, -1.0,
                         False, False, False, False] )




    #
    # Offline variables
    #


    trkCont  = elCont.trackParticle()
    hasTrack = True if trkCont.size()>0 else False
   
    # Offline Shower shapes
    event_row.append( elCont.et() )
    event_row.append( elCont.eta() )
    event_row.append( elCont.caloCluster().etaBE2())
    event_row.append( elCont.phi() )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rhad ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f3 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.weta2 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Rphi ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Reta ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.wtots1 ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.Eratio ) )
    event_row.append( elCont.showerShapeValue( EgammaParameters.f1 ) )
    # Offline track variables
    if hasTrack:
      event_row.append( hasTrack)
      event_row.append( trkCont.numberOfBLayerHits() ) # int
      event_row.append( trkCont.numberOfPixelHits() ) # int
      event_row.append( trkCont.numberOfTRTHits() ) # int
      event_row.append( trkCont.d0() )
      event_row.append( trkCont.d0significance() )
      event_row.append( trkCont.eProbabilityHT() )
      event_row.append( trkCont.trans_TRT_PID() )
      event_row.append( elCont.deta1() )
      event_row.append( elCont.dphi2() )
      event_row.append( elCont.deltaPhiRescaled2() )
      event_row.append( trkCont.DeltaPOverP() )
    else:
      event_row.extend( [False, -1, -1, -1, -1.0, -1.0, -1.0, 
                         -1.0, -1.0, -1.0, -1.0, -1.0] )


    # Adding Offline PID LH decisions
    event_row.append( elCont.accept( "el_lhtight"  ) )
    event_row.append( elCont.accept( "el_lhmedium" ) )
    event_row.append( elCont.accept( "el_lhloose"  ) )
    event_row.append( elCont.accept( "el_lhvloose" ) )
 

    #
    # Decorate from external funcions by the client. Can be any type
    #
    for feature, func, in self.__decorators.items():
      event_row.append( func(context) )



    #
    # Decorate with other decisions from emulator service
    #
    dec = context.getHandler("MenuContainer")
    for feature in self.__extra_features:
      passed = dec.accept(feature).getCutResult('Pass')
      event_row.append( passed )

    if len(event_row) != len( self.__event_label ):
      MSG_FATAL( "This event missing some column. We have some problem into the dumper code! please, verify it!")


    key = ('et%d_eta%d') % (etBinIdx, etaBinIdx)
    self.fill(key , event_row)
    return StatusCode.SUCCESS



  #
  # Finalize method
  #
  def finalize( self ):

    from Gaugi import save, mkdir_p
    mkdir_p( self.__outputname )

    for etBinIdx in range(len(self.__etbins)-1):
      for etaBinIdx in range(len(self.__etabins)-1):

        key =  'et%d_eta%d' % (etBinIdx,etaBinIdx)
        
        if self.__event[key] is None:
          continue

        # file output name
        ofile = self.__outputname+'/'+self.__outputname+"_"+key

        self.save( self.__event[key], self.__event_label, 
                   etBinIdx, etaBinIdx, ofile)
  
    return StatusCode.SUCCESS





  #
  # Prepare dataset
  #
  def save( self, data, features, etBinIdx, etaBinIdx, ofile):

      MSG_INFO(self, 'Saving... ' + ofile)

      # get type names from first event
      dtypes = np.array( self.get_types(data[0], features) )

      data = np.array(data)
      features = np.array(features)
      n_samples = data.shape[0]

      if data.shape[1] != len(features):
        MSG_FATAL( self, "number of columns is different than features. Abort! something is wrong!")


      # Loop over regions
      d = { 
            # data header
            "etBins"    : self.__etbins,
            "etaBins"   : self.__etabins,
            "etBinIdx"  : etBinIdx,
            "etaBinIdx" : etaBinIdx,
            "ordered_features" : features,
            #"ordered_dtypes": dtypes,
            }


      # Create float staff
      float_indexs = [ idx for idx, name in enumerate(dtypes) if 'float32' in name]
      data_float = data[:, float_indexs  ].astype('float32')
      features_float = features[float_indexs]

      # create bool staff
      bool_indexs = [ idx for idx, name in enumerate(dtypes) if 'bool' in name]
      data_bool = data[:, bool_indexs  ].astype(bool)
      features_bool = features[bool_indexs]

      # create int staff
      int_indexs = [ idx for idx, name in enumerate(dtypes) if 'int' in name]
      data_int = data[:, int_indexs].astype(int)
      features_int = features[int_indexs]

      # others
      object_indexs = [ idx for idx, name in enumerate(dtypes) if 'object' in name]
      data_object = data[: , object_indexs]
      features_object = features[object_indexs]


      d['data_float']       = data_float
      d['data_bool']        = data_bool
      d['data_int']         = data_int
      d['data_object']      = data_object
      d['features_float']   = features_float
      d['features_bool']    = features_bool
      d['features_int']     = features_int
      d['features_object']  = features_object
      d['target']           = np.ones( (n_samples,) ) * self.__target
      gc.collect()

      MSG_INFO( self, 'Saving (%d,%d) with : (%d,%d)', etBinIdx, etaBinIdx, 
                data_float.shape[0], len(features) )

      save(d, ofile, protocol = 'savez_compressed') # allow_pickle by default



  #
  # Get dtype names for each column
  #
  def get_types(self, row, features):
    # Fill dtypes
    dtypes = []
    for idx, feature in enumerate(features):
      if (type(row[idx]) is float) or (type(row[idx]) is np.float32):
        dtypes.append( 'float32' )
      elif type(row[idx]) is int:
        dtypes.append('int')
      elif type(row[idx]) is list:
        dtypes.append('object')
      elif type(row[idx]) is bool:
        dtypes.append('bool')
    return dtypes
